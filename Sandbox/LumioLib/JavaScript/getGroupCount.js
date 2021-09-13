function getGroupCount() {
    var all_ann = document.querySelector('.player-whiteboard.whiteboard-ready').wbp.pageModel.getVisibleTopLevelAnnotations()
    var groups = 0
    var nongroups = 0
    var cloners = 0
    var lockers = 0

    all_ann.forEach(ann => {
        if (ann.isGroup) {
            groups += 1
        }      
        else {
            nongroups += 1
        }

        if (ann.isCloner) {
            cloners += 1
        }

        if (ann.lock.any) {
            lockers += 1
        }

    });
    return [all_ann.length, groups, nongroups, cloners, lockers]
};

function looper() {
    var result = getGroupCount()
    if (result[0] == 4) {
        console.log("done")
    }else {
        console.log(result)
        setTimeout(looper, 1000)
    }
}

return getGroupCount()
