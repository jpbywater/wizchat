# Don't rename first_str() and to_user()
# If output_from = "Student" message will be sent directly to student (unless supervisor settings change this)
# If output_from = "Helpee" message will be sent to supervisor (unless no supervisor or supervisor settings change this)

def first_str():
    return "Hi! I've been given this question but I'm not sure how to answer it. Can you help me?"

def to_user(new_text, new_image, all_chat_data):
    # for testing....

    if new_text == "q":
        output_from = "Helpee"
    else:
        output_from = "Student"
    output_text = 'I heard you say: "' + new_text + '"'
    output_image = new_image  # placeholder
    return output_from, output_text, output_image




