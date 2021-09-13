function getClonerCount() {
    var all_ann = document.querySelector('.player-whiteboard.whiteboard-ready').wbp.pageModel.getVisibleTopLevelAnnotations()
    var isCloner = 0

    all_ann.forEach(ann => {
        if (ann.isCloner) {
            isCloner =+ 1
        }
    });

    return isCloner
};

return getClonerCount()