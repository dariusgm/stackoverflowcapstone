function rescaleFeature(feature, value) {
    return value / window.config.max_dict[feature]
}

function rescaleTarget(feature, value) {
    return value * window.config.max_dict[feature]
}

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

    // get value if selected, and allow resetting of checkbox
    var reset = [];
    var inputs = document.getElementsByTagName("input")
    for (var i = 0; i < inputs.length; i++) {
        var element = inputs[i]
        if (element.type === 'text') {
            var key = element.name.split("-")[0]
            var value = parseInt(element.value)
            var index = features.indexOf(key)

            // given not used any value input field, set the feature to 0
            if (isNaN(value)) {
                rawArray[index] = 0
            } else {
                reset.push(key)
                rawArray[index] = rescaleFeature(key, value)
            }
        }
    }

    // fill selected features with checkbox
    var inputs = document.getElementsByTagName("input")
    for (var i = 0; i < inputs.length; i++) {
        var element = inputs[i]
        if (element.type === 'checkbox' && element.checked) {
            var key = element.getAttribute("id")
            var value = element.value
            var lookupKey = key + "_" + value
            var index = features.indexOf(lookupKey)
            if (index == -1) {
                console.log("Feature not found")
            } else {
                if (reset.includes(key)) {
                    element.checked = false
                    rawArray[index] = 0
                    console.log("Feature resetted")
                } else {
                    rawArray[index] = 1
                }
            }
        }
    }

    var tensor = tf.tensor(rawArray, shape=[1, features.length])
    model.predict(tensor).data().then(function (e) {
        var scaledPrediction = rescaleTarget("ConvertedComp", e)
        if (scaledPrediction < 0) {
            alert("No Prediciton possible given the input data. Think you found a bug? Please write :-)")
        } else {
            alert("Your Prediction: " + Math.floor(scaledPrediction) + " USD per Year ")
        }
    })
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
