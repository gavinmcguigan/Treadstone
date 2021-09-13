

function getNonGroupCount() {
    var all_ann = document.querySelector('.player-whiteboard.whiteboard-ready').wbp.pageModel.getVisibleTopLevelAnnotations()
    var groups = 0
    var nongroups = 0

    all_ann.forEach(ann => {
        if (ann.isGroup) {
            groups =+ 1
        }
        
        else {
            nongroups += 1
        }
    });

    return nongroups
};




return getNonGroupCount()