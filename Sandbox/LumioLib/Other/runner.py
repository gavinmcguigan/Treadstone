from __future__ import with_statement
from queue import Queue
from threading import Thread
import subprocess
import argparse
import os
import urllib
import requests
import glob
import shlex
import sys
import platform
import xml.etree.ElementTree as ET


""" Refactored version of the shared-test/runner.py"""

# argument priorities (highest -> lowest): command line, environment var, config file(?)

class TeamcityConfig:
    def __init__(self, server=None, user=None, password=None, port='443'):
        dict_env = process_env_vars('TC')
        print("Values for [dict_env]:")
        for key, value in dict_env.items():
            print(f"    [{key}] => [{value}]")

        self.server = server if server is not None else dict_env['server']
        self.user = user if user is not None else dict_env['user']
        self.password = password if password is not None else dict_env['password']
        self.port = port if port is not None else dict_env['port']
        self.server_url = f"{self.server}:{self.port}"
        self.credential = (self.user, self.password)

        self.headers = {'accept': 'application/json'}       # Requests header for teamcity


class ProjectConfig:
    def __init__(self, project_id=None, config_id=None, outputdir=None, listener=None, source=None, run_total=None, mode=None, build_step=None):
        self.config_options = process_env_vars('RF')
        self.project_id = project_id if project_id is not None else self.config_options['variable']['project_id']
        self.build_step = build_step if build_step is not None else self.config_options['build_step']
        self.outputdir = outputdir if outputdir is not None else self.config_options['outputdir']
        self.config_options['source'] = source if source is not None else self.config_options['source']
        self.run_total = run_total if run_total is not None else self.config_options['run_total']
        self.mode = mode if mode is not None else self.config_options['mode']
        self.listener = listener if listener is not None else self.config_options['listener']
        self.config_id = config_id if config_id is not None else self.config_options['config_id']


class UnifiedRunner:
    def __init__(self, teamcity_config, project_config, include=None):
        self.teamcity_config = teamcity_config
        self.project_config = project_config

        self.mode = project_config.config_options.pop('mode')
        self.config_id = project_config.config_options.pop('config_id')
        self.source = project_config.config_options.pop('source')
        print(self.source)
        self.rerun_failed = project_config.config_options.pop('rerun_failed')
        try:
            self.rerun_suites = project_config.config_options.pop('rerun_suites')
        except:
            self.rerun_suites = '0'
        self.run_total = project_config.config_options.pop('run_total')
        self.shell = project_config.config_options.pop('shell')
        self.workpath = project_config.config_options.pop('workpath')
        self.build_step = project_config.config_options.pop('build_step')
        try:
            self.pabot_processes = project_config.config_options.pop('pabot_processes')
        except:
            self.pabot_processes = '2'
        try:
            self.pabot_pabotlib = project_config.config_options.pop('pabot_pabotlib')
        except:
            self.pabot_pabotlib = '0'
        try:
            self.pabot_suitesfrom = project_config.config_options.pop('pabot_suitesfrom')
        except:
            self.pabot_suitesfrom = '0'
        try:
            self.pabot_suitesto = project_config.config_options.pop('pabot_suitesto')
        except:
            self.pabot_suitesto = ''
        try:
            self.pabot_resourcefile = project_config.config_options.pop('pabot_resourcefile')
        except:
            self.pabot_resourcefile = ''

        project_config.config_options['include'] = include if include is not None else project_config.config_options['include']

        self.process_count = 0
        self.results = Queue()

        self.project_id = self.project_config.project_id
        self.credential = self.teamcity_config.credential
        print(os.getcwd())
        #try:
            #os.chdir(self.workpath + '\\' + self.project_id + '-test')
        #except:
        #    print "working directory does not exist."
        #print str(self.workpath) + '\\' + str(self.project_id) + '-test'
        #print os.getcwd()

    def start_remote_server(self):
        pass

    def stop_remote_server(self):
        pass

    def get_prev_version(self, build_id, branch):
        url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:"
        url = f"{url}{build_id}" if not branch else f"{url}{build_id},branch:name:{branch}"
        print(f"Getting previous version using url: {url}")
        response = requests.get(url)
        root = ET.fromstring(response.content)
        number = root.attrib['number']
        return number

    def get_current_version(self):
        file_name = glob.glob('.\\devops-knapsack/buildinfo_*.txt')[0]
        print (file_name)
        with open(file_name, 'r') as f:
            line = f.readline()
            version = line.strip("BuildNumber: ")
            version = version.strip("\n")
            return version
	
    def compare_versions(self, build_id, branch):
        try:
            prev = self.get_prev_version(build_id, branch)
        except Exception as e:
            print(f"Exception: {e}")
            # If no info for the branch can be found, assume the REST call requires no branch info
            prev = self.get_prev_version(build_id, None)
        current = self.get_current_version()
        if prev != current:
            print(f"##teamcity[buildStatus status='FAILURE' text='Version Mismatch: {prev} does not equal to: {current}]")
            sys.exit(1)
        else:
            print("Versions match, proceeding with rerunning.")

    def determine_last_branch(self, build_id, branch):
        # If '<default>' branch was run after 'branch' branch, set branch to '<default>'
        initial_branch = branch

        try:
            prev_branch = self.get_prev_version(build_id, branch)
            prev_branch_build = prev_branch.split(".")
        except Exception as e:
            print(f"Exception finding build for {branch} branch: {e}")
            prev_branch = 'unknown'
            prev_branch_build = [0, 0, 0]

        try:
            prev_none = self.get_prev_version(build_id, None)
            prev_none_build = prev_none.split(".")
        except Exception as e:
            print(f"Exception finding build for no branch: {e}")
            prev_none_build = [0, 0, 0]

        try:
            prev_default = self.get_prev_version(build_id, '<default>')
            prev_default_build = prev_default.split(".")
        except Exception as e:
            print(f"Exception finding build for default branch: {e}")
            prev_default_build = [0, 0, 0]

        if prev_default_build == prev_branch_build == [0, 0, 0]:
            branch = None
        elif int(prev_default_build[0]) < int(prev_branch_build[0]):
            pass
        elif int(prev_default_build[1]) < int(prev_branch_build[1]):
            pass
        elif int(prev_default_build[2]) > int(prev_branch_build[2]):
            print(f"prev_" + branch + "_build = " + str(prev_branch) + " and prev_default_build = " + str(prev_default))
            branch = '<default>'

        if branch != initial_branch:
            if branch is not None:
                print(f"Last branch changed from {initial_branch} to {branch}")
            else:
                print(f"Last branch changed from {initial_branch} to None")
        return branch

    def mock_test_stats(self, status_dict):
        for _ in range (0, int(status_dict['passed'])):
            print(f"\n##teamcity[testStarted name='p"+str(_)+"']")
            print(f"\n##teamcity[testFinished name='p"+str(_)+"']")
        try:
            for _ in range (0, int(status_dict['failed'])):
                print(f"\n##teamcity[testStarted name='f"+str(_)+"']")
                print(f"\n##teamcity[testIgnored name='f"+str(_)+"']")
                print(f"\n##teamcity[testFinished name='f"+str(_)+"']")
        except KeyError:
            print(f"\nNo failed tests, why are we running this?")

    def get_prev_status(self, build_id, branch):
        url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:"
        url = f"{url}{build_id}" if not branch else f"{url}{build_id},branch:name:{branch}"
        response = requests.get(url)
        status_dict = {}
        root = ET.fromstring(response.content)
        name = root.find('buildType').get('name')
        if (name == "hack-state-just-build"):
            return None
        status_text = root.find('statusText').text
        current = root.get('number')
        #print status_text
        if "Execution timeout" in status_text:
            print(f"\n##teamcity[buildStatus status='FAILURE' text='Previous run not valid']")
            sys.exit(1)
        if "Out of memory" in status_text:
            print(f"\n##teamcity[buildStatus status='FAILURE' text='Previous run not valid']")
            sys.exit(1)
        if "Version Mismatch" in status_text:
            print(f"\n##teamcity[buildStatus status='FAILURE' text='Previous run not valid']")
            sys.exit(1)
        status_text = status_text.lstrip('Tests ')
        status = status_text.split(', ')
        for field in status:
            if (field !=  'Success'):
                list = field.split(': ')
                if "new" in list[1]:
                    status_dict[list[0]] = list[1].rstrip("(")[0]
                else:
                    status_dict[list[0]] = list[1]
            else:
                return None
        return status_dict

    def get_prev_suites_status(self, build_id, outputdir, run, branch):
        status_dict = {}
        status0 = self.get_prev_stream_status(build_id, outputdir, '0', run, branch)
        try:
            status1 = self.get_prev_stream_status(build_id, outputdir, '1', run, branch)
            status_dict['passed'] = str( int(status0['passed']) + int(status1['passed']))
            status_dict['failed'] = str( int(status0['failed']) + int(status1['failed']))
        except:
            status_dict['passed'] = status0['passed']
            status_dict['failed'] = status0['failed']
        return status_dict

    def get_prev_stream_status(self, build_id, outputdir, stream, run, branch):
        output = outputdir.split("results/")[1]
        if branch is None:
            url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:" + str(build_id) + "/artifacts/content/" + str(output) + "/run"+str(run)+"/stream_"+str(stream)+"/output.xml"
        else:
            url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:" + str(build_id) + ",branch:name:" + str(branch)  + "/artifacts/content/" + str(output) + "/run"+str(run)+"/stream_"+str(stream)+"/output.xml"
        response = requests.get(url)
        status_dict = {}
        root = ET.fromstring(response.content)
        suite_stats = root.find('statistics').find('suite')
        suite_depth = 0
        for stat in suite_stats.iter('stat'):
            id = stat.attrib['id']
            count = id.count('-')
            if count > suite_depth:
                suite_depth = count
        total_passed = 0
        total_failed = 0
        for stat in suite_stats.iter('stat'):
            id = stat.attrib['id']
            count = id.count('-')
            if count == suite_depth:
                passed = int(stat.attrib['pass'])
                failed = int(stat.attrib['fail'])
                if failed > 0:
                    failed = failed + passed
                    passed = 0
                total_passed += passed
                total_failed += failed
        status_dict['passed'] = str(total_passed)
        status_dict['failed'] = str(total_failed)
        return status_dict

    def get_prev_run_total(self, build_id, branch):
        url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:"
        url = f"{url}{build_id}" if not branch else f"{url}{build_id},branch:name:{branch}"
        response = requests.get(url)
        root = ET.fromstring(response.content)
        found = False
        properties = root.find("properties")
        for property in properties.iter("property"):
            if property.attrib["name"] == "env.RF_RUN_TOTAL":
                prev_run_total = property.attrib["value"]
                found = True
        if found == False:
            print(f"Previous run total not found, setting to 1")
            prev_run_total = "1"
        return prev_run_total

    def get_prev_xml(self, build_id, outputdir, stream, run, branch):
        output = outputdir.split("results/")[1]
        if branch is None:
            url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:" + str(build_id) + "/artifacts/content/" + str(output) + "/run"+str(run)+"/stream_"+str(stream)+"/output.xml"
        else:
            url = "https://amptest_teamcity_srvc:monkey99coffee@ampcity.smarttech-prod.com/httpAuth/app/rest/builds/buildType:" + str(build_id) + ",branch:name:" + str(branch) + "/artifacts/content/" + str(output) + "/run"+str(run)+"/stream_"+str(stream)+"/output.xml"
        location = os.path.relpath(outputdir+"/run0/stream_"+str(stream))
        file_path = location+"/output.xml"
        print(url)
        if not os.path.exists(location):
            os.makedirs(location)
        try:
            file = urllib.URLopener()
            file.retrieve(url, file_path)
        except:
            print("Download Unsuccessful.")
            pass


    # Multiprocess and rerun logic
    def run_tests(self, dry_run=False):
        config_options = self.project_config.config_options
        streams = list(str(self.mode))

        list_streams = list()
        dict_streams = dict()
        procs = list()
        streams_current_run = list()
        if self.rerun_failed == '1' or self.pabot_suitesfrom == '1':
            if self.config_id is None:
                print(f"Build Id is not available, cannot retrieve past artifacts.")
            else:
                if 'branch' in config_options['variable']:
                    branch = config_options['variable']['branch'].replace("refs/heads/", "")
                    # This code (3 subsequent lines) was breaking rerun on failed on suite.smarttech.com Production pipeline.
                    #if "master" in branch:
                    #    branch = branch.replace("master", "<default>")
                    #    print "Switching branch name from master to <default>"
                else:
                    branch = None
                if self.rerun_failed == '1':
                    branch = self.determine_last_branch(self.config_id, branch)
                    self.compare_versions(self.config_id, branch)
                prev_final_run = self.get_prev_run_total(self.config_id, branch)
                status = self.get_prev_status(self.config_id, branch)
                if self.rerun_suites == '0':
                    status = self.get_prev_status(self.config_id, branch)
                else:
                    status = self.get_prev_suites_status(self.config_id, outputdir, str(prev_final_run), branch)
                self.mock_test_stats(status)
                self.get_prev_xml(self.config_id, config_options['outputdir'], '0', str(prev_final_run), branch)
                self.get_prev_xml(self.config_id, config_options['outputdir'], '1', str(prev_final_run), branch)

        for idx, stream in enumerate(streams):
            remote = 'false' if stream == '0' else 'true'
            dict_current_stream = {'remote': remote, 'current_run': 1, 'name': 'stream_'+str(idx), 'index': idx}
            list_streams.append(dict_current_stream)
            try:
                proc = self.create_test_stream(stream_name=dict_current_stream['name'], run=str(dict_current_stream['current_run']), remote=dict_current_stream['remote'], **config_options)
                procs.append(proc)
            except:
                pass

        while self.process_count > 0:
            description, rc = self.results.get()
            print("job", description, "ended with rc =", rc)
            self.process_count-= 1
            print(self.process_count)
            if rc != 0 and rc <= 250:
                stream_index = int(description.split("_")[1])
                print(f'stream_index is: {stream_index}')
                if list_streams[stream_index]['current_run'] < int(self.run_total):
                    list_streams[stream_index]['current_run'] += 1
                    proc = self.create_test_stream(stream_name=list_streams[stream_index]['name'], remote=str(list_streams[stream_index]['remote']), run=str(list_streams[stream_index]['current_run']), **config_options)
                    procs.append(proc)
                else:
                    print(list_streams[stream_index]['name'] + ' has ended.')

    # Creates the test process based on configuration
    def create_test_stream(self, stream_name, run, remote, **options):
        #  use path join later
        if 'pabot' in self.shell:
            options['verbose'] = True
            options['processes'] = str(self.pabot_processes)
            if self.pabot_pabotlib == '1':
                options['pabotlib'] = True
            if self.pabot_suitesfrom == '1':
                options['suitesfrom'] = options['outputdir'] + '/' + self.build_step + '/run' + str(int(run)-1) + '/'+stream_name + '/output.xml'
            if self.pabot_suitesto != '':
                options['suitesto'] = self.pabot_suitesto
            if self.pabot_resourcefile != '':
                options['resourcefile'] = self.pabot_resourcefile

        if int(run) > 1 or self.rerun_failed == '1':
            if self.rerun_suites == '0':
                options['runfailed'] = options['outputdir'] + '/' + self.build_step + '/run' + str(int(run)-1) + '/'+stream_name + '/output.xml'
            else:
                options['rerunfailedsuites'] = options['outputdir'] + '/' + self.build_step + '/run' + str(int(run)-1) + '/' + stream_name + '/output.xml'

        options['outputdir'] = options['outputdir'] + '/' + self.build_step + '/run'+run+'/'+stream_name

        options['settag'] = ['run'+str(run), 'runtotal' + str(self.run_total)]  # adding the correct run count and run total to the test

        if 'pabot' in self.shell:
            options['settag'].append('poolid_${PABOTEXECUTIONPOOLID}')

        if len(self.mode) > 1:
            options['include'] = options['include'] + 'AND' + stream_name

        #  Modifies the listener arguments
        options['listener'] = options['listener'] + ':' + stream_name

        command_line = ' '
        seq = (self.shell, convert_options_to_command_line(**options), self.source)

        raw = shlex.split(command_line.join(seq))
        print(raw)
        proc = subprocess.Popen(command_line.join(seq), shell=True)
        self.process_count += 1
        Thread(target=process_waiter, args=(proc, stream_name, self.results)).start()
        return proc


def process_waiter(popen, description, que):
    try:
        popen.wait()
    finally:
        que.put((description, popen.returncode))


def process_env_vars(prefix):
    dict_env = dict()
    prefix += '_'  # Consider using string separators instead
    dict_env['variable'] = dict()
    len(prefix)
    if platform.system() == 'Windows':
        os.environ['RF_VAR_OSRUN'] = 'win'
    elif platform.system() == 'Darwin':
        os.environ['RF_VAR_OSRUN'] = 'mac'
    try:
        if os.getenv('RF_VAR_OSVERSION', None) is None:
            if platform.release() == '8':
                os.environ['RF_VAR_OSVERSION'] = '8'
            elif platform.release() == '10':
                os.environ['RF_VAR_OSVERSION'] = '10'
            elif platform.release() == '7':
                os.environ['RF_VAR_OSVERSION'] = '7'
            elif platform.release().startswith('18'):
                os.environ['RF_VAR_OSVERSION'] = '14'  # for mac 10.14
            elif platform.release().startswith('17'):
                os.environ['RF_VAR_OSVERSION'] = '13'  # for mac 10.13
            elif platform.release().startswith('16'):
                os.environ['RF_VAR_OSVERSION'] = '12' # for mac 10.12
            elif platform.release().startswith('15'):
                os.environ['RF_VAR_OSVERSION'] = '11' # for mac 10.11
            elif platform.release().startswith('14'):
                os.environ['RF_VAR_OSVERSION'] = '10'  # for mac 10.10
            elif platform.release().startswith('13'):
                os.environ['RF_VAR_OSVERSION'] = '9'  # for mac 10.9

    except:
        print("unsupported OS version!")
        raise

    for key in os.environ.keys():
        if prefix in key:  # consider changing to regex
            if "_VAR_" in key:  # parses variables
                dict_env['variable'][(key[len(prefix)+4:].lower())] = os.environ[key]
            else:
                dict_env[key[len(prefix):].lower()] = os.getenv(key, None)
    if len(dict_env['variable']) == 0:
        dict_env.pop('variable')
    return dict_env

def convert_options_to_command_line(**options):
    commandline = ''

    if 'verbose' in options:   # pabot command-line options are required to go before other robot framework command-line options
       options.pop('verbose')
       commandline = commandline + '--verbose '
       commandline = commandline + '--processes ' + str(options.pop('processes')) + ' '
       if 'pabotlib' in options:
           commandline = commandline + '--pabotlib '
           options.pop('pabotlib')
       if 'suitesfrom' in options:
           commandline = commandline + '--suitesfrom ' + str(options.pop('suitesfrom')) + ' '
       if 'suitesto' in options:
           commandline = commandline + '--suitesto ' + str(options.pop('suitesto')) + ' '
       if 'resourcefile' in options:
           commandline = commandline + '--resourcefile ' + str(options.pop('resourcefile')) + ' '

    for key, value in options.items():
        if key is 'variable':  # parse variables (dict)
            for item in value.keys():
                commandline = commandline + '--'+str(key) + ' ' + str(item)+':'+str(value[item]) + ' '
        elif key is 'settag':  # parse tags (list)
            for tag in value:
                commandline = commandline + '--settag ' + str(tag) + ' '
        elif key is 'runfailed': #workaround for robotframework 3.0 where --runfailed -> --rerunfailed
            commandline = commandline + '-R' + ' ' + str(value) + ' '
        else:
            commandline = commandline + '--'+str(key) + ' ' + str(value) + ' '
    return commandline.rstrip()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Test Running Parameters')
    parser.add_argument('--outputdir', default=None)
    parser.add_argument('--include', default=None)
    parser.add_argument('--exclude', default=None)
    parser.add_argument('--project_id', default=None)
    parser.add_argument('--webenv', default=None)
    parser.add_argument('--browser', default=None)
    parser.add_argument('--source', default=None)
    parser.add_argument('--run_total', default=None)
    parser.add_argument('--listener', default=None)
    parser.add_argument('--name', default=None)
    parser.add_argument('--mode', default=None)
    parser.add_argument('--server', default=None)
    parser.add_argument('--port', default=None)
    parser.add_argument('--user', default=None)
    parser.add_argument('--password', default=None)
    parser.add_argument('--config_id', default=None)
    parser.add_argument('--build_step', default=None)

    args = vars(parser.parse_args())
    outputdir = args['outputdir']
    include = args['include']
    project_id = args['project_id']
    browser = args['browser']
    webenv = args['webenv']
    exclude = args['exclude']
    source = args['source']
    run_total = args['run_total']
    listener = args['listener']
    name = args['name']
    mode = args['mode']
    user = args['user']
    password = args['password']
    server = args['server']
    port = args['port']
    config_id = args['config_id']
    build_step = args['build_step']

    print("Values for [args]:")
    for key, value in args.items():
        print(f"    [{key}] => [{value}]")

    teamcity_config = TeamcityConfig(server, user, password, port)
    project_config = ProjectConfig(project_id, config_id, outputdir, listener, source, run_total, mode, build_step=build_step)
    unified_runner = UnifiedRunner(teamcity_config, project_config, include=include)
    unified_runner.run_tests()
