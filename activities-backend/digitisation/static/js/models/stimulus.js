$(document).ready(function($) {
    var triggerField = $("#id_stimulus_type");
    var targetField = {
        document: $("#id_document"),
        document_resource_id: $("#id_document_resource_id"),
        document_uriref: $("#id_document_uriref"),
        text: $("#id_text"),
        image: $("#id_image"),
        image_resource_id: $("#id_image_resource_id"),
        image_uriref: $("#id_image_uriref"),
        image_preview: $(".field-image_preview"),
        questionnaire: $("#id_questionnaire"),
        questionnaire_wp_post: $("#id_questionnaire_wp_post"),
        questionnaire_wp_form: $("#id_questionnaire_wp_form"),
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
                targetField.document.closest(".form-row").hide();
                targetField.document_resource_id.closest(".form-row").hide();
                targetField.document_uriref.closest(".form-row").hide();
                targetField.text.closest(".form-row").hide();
                targetField.image.closest(".form-row").hide();
                targetField.image_resource_id.closest(".form-row").hide();
                targetField.image_uriref.closest(".form-row").hide();
                targetField.image_preview.closest(".form-row").hide();
                targetField.questionnaire.closest(".form-row").show();
                targetField.questionnaire_wp_post.closest(".form-row").show();
                targetField.questionnaire_wp_form.closest(".form-row").show();
                break;
            case "Image":
                targetField.document.closest(".form-row").hide();
                targetField.document_resource_id.closest(".form-row").hide();
                targetField.document_uriref.closest(".form-row").hide();
                targetField.text.closest(".form-row").hide();
                targetField.image.closest(".form-row").show();
                targetField.image_resource_id.closest(".form-row").show();
                targetField.image_uriref.closest(".form-row").show();
                targetField.image_preview.closest(".form-row").show();
                targetField.questionnaire.closest(".form-row").hide();
                targetField.questionnaire_wp_post.closest(".form-row").hide();
                targetField.questionnaire_wp_form.closest(".form-row").hide();
                break;
            case "Document":
            case "Segment":
                targetField.document.closest(".form-row").show();
                targetField.document_resource_id.closest(".form-row").show();
                targetField.document_uriref.closest(".form-row").show();
                targetField.text.closest(".form-row").show();
                targetField.image.closest(".form-row").hide();
                targetField.image_resource_id.closest(".form-row").hide();
                targetField.image_uriref.closest(".form-row").hide();
                targetField.image_preview.closest(".form-row").hide();
                targetField.questionnaire.closest(".form-row").hide();
                targetField.questionnaire_wp_post.closest(".form-row").hide();
                targetField.questionnaire_wp_form.closest(".form-row").hide();
                break;
            default:
                targetField.document.closest(".form-row").hide();
                targetField.document_resource_id.closest(".form-row").hide();
                targetField.document_uriref.closest(".form-row").hide();
                targetField.text.closest(".form-row").hide();
                targetField.image.closest(".form-row").hide();
                targetField.image_resource_id.closest(".form-row").hide();
                targetField.image_uriref.closest(".form-row").hide();
                targetField.image_preview.closest(".form-row").hide();
                targetField.questionnaire.closest(".form-row").hide();
                targetField.questionnaire_wp_post.closest(".form-row").hide();
                targetField.questionnaire_wp_form.closest(".form-row").hide();
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
