
function buttonClicked(e) {
    e.preventDefault()
    var locked = []
    var features = window.config['feature_list']
    var rawArray = new Array(features.length)

    // Initialize feature tensor
    for (var i = 0; i < features.length; i++) {
        rawArray[i] = 0;
    }

    // fill selected features, start with select box
    var selects = document.getElementsByTagName("select")
    for (var i = 0; i < selects.length; i++) {
        var element = selects[i]
        var key = element.getAttribute("id")
        var value = element.options[element.selectedIndex].value
        var lookupKey = key + "_" + value
        var index = features.indexOf(lookupKey)
        if (index == -1) {
            console.log("Feature not found")
        } else {
            rawArray[index] = 1
        }
    }

    // fill selected features with checkbox
    var checkboxes = document.getElementsByTagName("input")
    for (var i = 0; i < checkboxes.length; i++) {
        var element = checkboxes[i]
        if (element.type === 'checkbox' && element.checked) {
            var key = element.getAttribute("id")
            var value = element.value
            var lookupKey = key + "_" + value
            var index = features.indexOf(lookupKey)
            if (index == -1) {
                console.log("Feature not found")
            } else {
                rawTensor[index] = 1
            }
        }
    }

    var tensor = tf.tensor(rawArray, shape=[1, features.length])
    var prediction = model.predict(tensor)
    console.log(prediction)



}

function registerEventHandler(e) {
    tf.loadLayersModel(config.model_path).then(function (e) {
        window.model = e
        console.log("Loaded Model")
    })
    
    window.document.getElementById("submit").addEventListener("click", function (e) {
        buttonClicked(e)
    })
}

window.document.addEventListener("DOMContentLoaded", registerEventHandler, false);
