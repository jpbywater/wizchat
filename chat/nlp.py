# Don't rename start_chat_msg() and to_user()
# If output_from = "Student" message will be sent directly to student (unless supervisor settings change this)
# If output_from = "Helpee" message will be sent to supervisor (unless no supervisor or supervisor settings change this)

def start_chat_msg():
    first_text = "Hello! I've been given this question but I'm not sure how to answer it. Can you help me?"
    first_img = {'ol': '5', 'ow': '4', 'oh': '3', 'sf': '1'}
    return {'from': 'Student', 'text': first_text, 'image': first_img}


def to_user(new_text, new_image, all_chat_data, trial_id):
    # for testing....

    if new_text == "q":
        output_from = "Helpee"
    else:
        output_from = "Student"
    output_text = 'I heard you say: "' + new_text + '"'
    output_image = new_image  # placeholder
    return output_from, output_text, output_image




