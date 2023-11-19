import gradio as gr
import pickle

filename = 'GBR-insurance-prediction.sav'
loaded_model = pickle.load(open(filename, 'rb'))


def age_group_selector(age_grp):
  if age_grp == '18-24': return [1,0,0,0,0,0,0,0]
  elif age_grp =='25-30':return [0,1,0,0,0,0,0,0]
  elif age_grp =='31-36':return [0,0,1,0,0,0,0,0]
  elif age_grp =='37-42':return [0,0,0,1,0,0,0,0] 
  elif age_grp =='43-48':return [0,0,0,0,1,0,0,0]
  elif age_grp =='49-54':return [0,0,0,0,0,1,0,0]
  elif age_grp =='54-60':return [0,0,0,0,0,0,1,0]
  elif age_grp =='61-64':return [0,0,0,0,0,0,0,1]
  elif age_grp =='64+:': return [0,0,0,0,0,0,0,1]
  
def bmi_selector(bmi):
  if bmi == '0-18.4 (Underweight)':return [1,0,0,0,0]
  elif bmi == '18.5-24.9 (Healthy Weight)':return [0,1,0,0,0]
  elif bmi == '25.0-29.9 (Overweight)':return [0,0,1,0,0]
  elif bmi == '30-39.0 (Obese)': return [0,0,0,1,0]
  elif bmi == '40+ (Severely Obese)': return [0,0,0,0,1]



def predict_insurance(sex,smoker,children,age_grp,bmi):
    
    to_predict = []
    
    if sex == 'male':
      to_predict.append(1)
    else:
      to_predict.append(0)

    if smoker == 'yes':
      to_predict.append(1)
    else:
      to_predict.append(0)

    to_predict.append(children)

    to_predict = to_predict + age_group_selector(age_grp)
    
    to_predict = to_predict + bmi_selector(bmi)
    
    return (loaded_model.predict([to_predict]))
    # return to_predict
    
css = """
footer {display:none !important}
.output-markdown{display:none !important}

.gr-button-lg {
    z-index: 14;
    width: 113px;
    height: 30px;
    left: 0px;
    top: 0px;
    padding: 0px;
    cursor: pointer !important; 
    background: none rgb(17, 20, 45) !important;
    border: none !important;
    text-align: center !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: rgb(255, 255, 255) !important;
    line-height: 1 !important;
    border-radius: 6px !important;
    transition: box-shadow 200ms ease 0s, background 200ms ease 0s !important;
    box-shadow: none !important;
}
.gr-button-lg:hover{
    z-index: 14;
    width: 113px;
    height: 30px;
    left: 0px;
    top: 0px;
    padding: 0px;
    cursor: pointer !important; 
    background: none rgb(37, 56, 133) !important;
    border: none !important;
    text-align: center !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: rgb(255, 255, 255) !important;
    line-height: 1 !important;
    border-radius: 6px !important;
    transition: box-shadow 200ms ease 0s, background 200ms ease 0s !important;
    box-shadow: rgb(0 0 0 / 23%) 0px 1px 7px 0px !important;
}
"""
with gr.Blocks(title="Insurance Price Prediction | Data Science Dojo", css=css) as demo:
    with gr.Row():
        input_sex = gr.Radio(["male", "female"],label="Sex")
        input_smoker = gr.Radio(["yes", "no"],label="Smoker")
    with gr.Row():    
        input_children = gr.Slider(0, 5,label='Children',step=1)
    with gr.Row():
        input_age_group = gr.Dropdown(['18-24','25-30','31-36','37-42','43-48','49-54','54-60','61-64','64+'],label='Age Group')
    with gr.Row():
        input_bmi = gr.Dropdown(['0-18.4 (Underweight)','18.5-24.9 (Healthy Weight)','25.0-29.9 (Overweight)','30-39.0 (Obese)','40+ (Severely Obese)'],label='BMI Range')
    with gr.Row():
        insurance = gr.Textbox(label='Estimated Insurance')
    btn_ins = gr.Button(value="Submit")
    btn_ins.click(fn=predict_insurance, inputs=[input_sex,input_smoker,input_children,input_age_group,input_bmi], outputs=[insurance])


demo.launch()