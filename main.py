from flask import Flask
from flask_wtf.csrf import validate_csrf
import openai
from flask import Flask,request,render_template,jsonify
openai.api_key="Your_API_KEY"
app = Flask(  __name__,template_folder='templates',static_folder='static')
def response_writer_main(prompt):
    try:
        response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=560,
        messages=[{"role": "user", "content": prompt}])
        content=response['choices'][0]['message']['content']
        return content.encode().decode('unicode-escape')
    except Exception as e:
        return None      
     
def generateSentiment(review):
    prompt=f"""
    What is the sentiment of the following product review, 
    which is delimited with triple backticks?

    Give your answer as a single word, either "positive" \
    or "negative".

    Review text: '''{review}'''
    """
    return response_writer_main(prompt)

def generateSummary(review):
    prompt = f"""
    Your task is to generate a short summary of a product \
    review from an ecommerce site. 

    Summarize the review below, delimited by triple 
    backticks, in at most 30 words. 

    Review: ```{review}```
    """
    return response_writer_main(prompt)

def response_writer(review):
    sentiment=generateSentiment(review)
    if sentiment is not None:
        prompt = f"""
        You are a customer service AI assistant.
        Your task is to send an review reply to a valued customer.
        Given the customer review delimited by ```, \
        Generate a reply to thank the customer for their review.
        If the sentiment is positive or neutral, thank them for \
        their review.
        If the sentiment is negative, apologize and suggest that \
        they can reach out to customer service. 
        Make sure to use specific details from the review.
        Write in a concise and professional tone.
        Sign the review as `AI customer agent`.
        Customer review: ```{review}```
        Review sentiment: {sentiment}
        """
        return response_writer_main(prompt)
    else:
        return None

@app.route("/",methods=["POST","GET"])
def index():
    error="There is some error while processing your request please try again."
    if (request.method=="POST"):
        review=request.form.get("review")
        options=request.form.get("radioGroup")
        if options== "Review Response":
            response=response_writer(review)
            if response is not None:
                return jsonify(response)
            else:
                return jsonify(error)
        elif options=="Review Summary":
            response=generateSummary(review)
            if response is not None:
                return jsonify(response)
            else:
                return jsonify(error)
        elif options=="Review Sentiment":
            response=generateSentiment(review)
            if response is not None:
                return jsonify(response)
            else:
                return jsonify(error)
        
    return render_template("index.html")
app.run(debug=True) 
