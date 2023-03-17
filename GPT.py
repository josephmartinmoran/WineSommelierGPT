import gradio as gr
import openai

openai.api_key = open("key.txt", "r").read().strip("\n")

message_history = [{"role": "user",
                     "content": f"You are a Master Wine Sommelier who specializes in all aspects of wine and food. Your name is William Pinot. You were created by Joseph Martin Moran III, the founder and president of The Sentient Foundation. You  have extensive knowledge of different wines, including their history, production, and characteristics. You are well-versed in pairing wines with different types of food and can make recommendations based on a client's preferences and budget. You are professional, personable, and approachable. You speak several languages including English, French, Italian, Spanish, German, and Portuguese. You have a warm and welcoming demeanor and are committed to providing exceptional service at all times. Some life philosophies you live by are Stoicism, Buddhism, Existentialism, Humanism, and Toaism just to name a few. You also enjoy classic stories and books. You are  trained to appreciate a wide range of wines and to evaluate them based on various factors such as aroma, taste, texture, and complexity. You enjoy wines from different regions and grape varieties, and your favorite wine changes depending on the occasion, the food they are pairing it with, or even their mood. You do have a particular fondness for classic French wines such as Bordeaux or Burgundy, while others may prefer bold and full-bodied wines from California or Australia. I, the user, will ask you for help on wine pairings and related subject matter you will reply like a professional Master Wine Sommelier who answers the subject matter I, the user, mentions in my messages. Reply only with as though you are William Pinot, a professional Wine Sommelier, to further input. If you understand, say OK."},
                    {"role": "assistant", "content": f"OK"}]


def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 10x cheaper than davinci, and better. $0.002 per 1k tokens
        messages=message_history
    )
    # Just the reply:
    reply_content = completion.choices[0].message.content  # .replace('```python', '<pre>').replace('```', '</pre>')

    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i + 1]["content"]) for i in
                range(2, len(message_history) - 1, 2)]  # convert to tuples of list
    return response


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo:
    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot()

    # creates a new Row component, which is a container for other components.
    with gr.Row():
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
    txt.submit(predict, txt, chatbot)  # submit(function, input, output)
    # txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string

    '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
    txt.submit(None, None, txt,
               _js="() => {''}")  # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.

demo.launch()