$(document).ready(function($) {
    var triggerField = $("#id_stimulus_type");
    var targetField = {
        text: $("#id_text"),
        image: $("#id_image"),
        image_resource_id: $("#id_image_resource_id"),
        image_uriref: $("#id_image_uriref"),
        questionnaire: $("#id_questionnaire"),
    };

    // Initial visibility state
    toggleFieldVisibility(triggerField.val());

    // Add a change event listener to the trigger field
    triggerField.on("change", function() {
        toggleFieldVisibility($(this).val());
    });

    // Function to toggle visibility of the target field
    function toggleFieldVisibility(triggerValue) {
        switch(triggerValue) {
            case "Questionnaire":
                targetField.text.closest(".form-row").hide();
                targetField.image.closest(".form-row").hide();
                targetField.image_resource_id.closest(".form-row").hide();
                targetField.image_uriref.closest(".form-row").hide();
                targetField.questionnaire.closest(".form-row").show();
                break;
            case "Image":
                targetField.text.closest(".form-row").hide();
                targetField.image.closest(".form-row").show();
                targetField.image_resource_id.closest(".form-row").show();
                targetField.image_uriref.closest(".form-row").show();
                targetField.questionnaire.closest(".form-row").hide();
                break;
            case "Document":
            case "Segment":
                targetField.text.closest(".form-row").show();
                targetField.image.closest(".form-row").hide();
                targetField.image_resource_id.closest(".form-row").hide();
                targetField.image_uriref.closest(".form-row").hide();
                targetField.questionnaire.closest(".form-row").hide();
                break;
            default:
                targetField.text.closest(".form-row").hide();
                targetField.image.closest(".form-row").hide();
                targetField.image_resource_id.closest(".form-row").hide();
                targetField.image_uriref.closest(".form-row").hide();
                targetField.questionnaire.closest(".form-row").hide();
                break;
        };
    };

/*
    // Get the field elements
    var wordpressPostField = $('#id_questionnaire');
    wordpressPostField.empty();

    // Make an AJAX request to fetch WordPress posts from a specific category
    $.ajax({
        url: 'https://platform.vast-project.eu/wp-json/wp/v2/posts?categories=18',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            // Clear previous options
            wordpressPostField.empty();

            // Populate the WordPress posts into the field
            $.each(data, function(index, post) {
                wordpressPostField.append($('<option>', {
                    value: post.id,
                    text: post.title.rendered
                }));
            });
        }
    });
*/
});