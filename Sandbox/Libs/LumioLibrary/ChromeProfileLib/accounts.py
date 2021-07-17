slso_tests = [
    ("slso.teacher1.auto@smartwizardschool.com", "Smart!23"),
    ("slso.teacher2.auto@smartwizardschool.com", "Smart!23"),
    ("slso.teacher5.auto@smartwizardschool.com", "Smart!23"),
    ("slso.teacher15.auto@smartwizardschool.com", "Smart!23"),
    ("slso.teacher16.auto@smartwizardschool.com", "Smart!23"),
    # ("slso.student6.auto@smartwizardschool.com", "Smart!23"),
    ]

slso_tests2 = []

lw_tests = []

ws_tests = []

lc_tests = []

handout_tests = []

teacher_share_tests = []

ms_teams_tests = []

google_tests = []

purchase_test_accounts = [
    ("slso.purchase.aus@smartwizardschool.com"),
    ("slso.purchase.uk@smartwizardschool.com"),
    ("slso.purchase.us@smartwizardschool.com"),
    ("slso.purchase.ca@smartwizardschool.com"),
]





































































accounts = [
"slso.teacher.auto@outlook.com",
"slso.teacher17.auto@smartwizardschool.com",
"slso.teacher7.auto@smartwizardschool.com",
"slso_teacher12@smartwizardschool.com",
"lw.autotest7.teacher@smartwizardschool.com",
"jlouie.autotest.2@smartwizardschool.com",
"slso.ws.teacher1.prod@outlook.com",
"slso.student2.auto@smartwizardschool.com",
"slso.student5.auto@smartwizardschool.com",
"labtest.denman.teacher@smartwizardschool.com",
"slso.student3.auto@smartwizardschool.com",
"slso.compat.file.test@smartwizardschool.com",
"slso.teacher18.auto@smartwizardschool.com",
"slso.teacher10@smartwizardschool.com",
"slso.ws.teacher2.auto@smartwizardschool.com",
"slso.teacher12@smartwizardschool.com",
"slso.teacher1.auto@smartwizardschool.com",
"lw.autotest1.teacher@smartwizardschool.com",
"slso.student6.auto@smartwizardschool.com",
"lw.autotest4.teacher@smartwizardschool.com",
"slso.compat.test@smartwizardschool.com",
"lw.autotest2.teacher@smartwizardschool.com",
"jlouie.autotest.3@smartwizardschool.com",
"slso.teacher5.new.auto@smartwizardschool.com",
"slso.teacher8.auto@smartwizardschool.com",
"slso.slo.teacher1@smartwizardschool.com",
"slso.teacher9.auto@smartwizardschool.com",
"slso.student8.auto@smartwizardschool.com",
"slso.slo.teacher13@smartwizardschool.com",
"slso.teacher11@smartwizardschool.com",
"slso.teacher.auto@zeususertest.onmicrosoft.com",
"slso.teacher14.auto@smartwizardschool.com",
"slso.teacher2.prod@smartwizardschool.com ",
"slso.teacher4.auto@smartwizardschool.com",
"slso.teacher.new.auto@smartwizardschool.com",
"slso.teacher13.auto@smartwizardschool.com",
"jlouie.autotest.1@smartwizardschool.com",
"slso.ws.teacher1.auto@smartwizardschool.com",
"slso.slo.teacher2@smartwizardschool.com",
"lw.autotest10.teacher@smartwizardschool.com",
"slso.teacher20.auto@smartwizardschool.com",
"slso_auto_29.1_handout@smartwizardschool.com",
"slso.teacher3.auto@smartwizardschool.com",
"slso.teacher2.auto@smartwizardschool.com",
"slso.teacher19.auto@smartwizardschool.com",
"lw.autotest8.teacher@smartwizardschool.com",
"slso.ws.teacher3.auto@smartwizardschool.com",
"slso.teacher6.auto@smartwizardschool.com",
"slso.slo.teacher11@smartwizardschool.com",
"slso.teacher5.auto@smartwizardschool.com",
"lw.autotest9.teacher@smartwizardschool.com",
"admin.autotest.id@smartwizardschool.com",
"slso.student7.auto@smartwizardschool.com",
"slso.teacher.auto@smarttech.com",
"slso.ws.teacher2.prod@outlook.com",
"slso_auto_29.0_handout@smartwizardschool.com",
"lw.autotest5.teacher@smartwizardschool.com",
"lw.autotest3.teacher@smartwizardschool.com",
"slso.teacher1.prod@smartwizardschool.com",
"slso.slo.teacher12@smartwizardschool.com",
"lw.autotest11.teacher@smartwizardschool.com",
"slso.content.teacher@smartwizardschool.com",
"slso.ws.teacher2.prod@smartwizardschool.com",
"slso.teacher16.auto@smartwizardschool.com",
"slso.ws.teacher1.prod@smartwizardschool.com",
"slso_auto_29.2_handout@smartwizardschool.com",
"slso.teacher15.auto@smartwizardschool.com",
"slso.slo.teacher10@smartwizardschool.com",
"slso.static.auto@smartwizardschool.com",
"slso.slo.teacher14@smartwizardschool.com",
"slso.student1.auto@smartwizardschool.com",
"slso_auto_29.3_handout@smartwizardschool.com",
"slso.student4.auto@smartwizardschool.com",
"lw.autotest6.teacher@smartwizardschool.com",
]

# ${slso_user_password}    Smart!23
# ${slso_user_password_outlook}    Sm@rt123
# ${slso_user_password_smarttech}    Smart@123
# ${slso_user_nonfederated_ms_pwd}    Smart!23
# ${lw_teacher_password}    grade7teacher
# ${slso_ws_teacher_password}    Smart!23


def get_all_accounts():
    return accounts 

def main():
    print(len(accounts))
    print(len(set(accounts)))

    for a in set(accounts):
        print(f'"{a}",')


if __name__ == "__main__":
    main()


