import gradio as gr
import requests
import os

from dotenv import load_dotenv 
load_dotenv() 

API_KEY = os.getenv("STABILITY_API_KEY")
API_ENDPOINT = os.getenv("STABILITY_API_ENDPOINT")

def generate_3d_model(image_file_path):
    try:
        response = requests.post(
            API_ENDPOINT,
            headers={
                "authorization": f"Bearer {API_KEY}",
            },
            files={
                "image": open(image_file_path, "rb")
            },
            data={},
        )

        if response.status_code == 200:
            output_path = "./output/output.glb"
    
            os.makedirs("./output", exist_ok=True)
            
            with open(output_path, 'wb') as file:
                file.write(response.content)
            
            return output_path, ""
        else:
            return None, f"Error: {response.status_code} - {response.json().get('errors', 'Unknown error')}"
    except Exception as e:
        return None, f"Exception occurred: {str(e)}"

iface = gr.Interface(
    fn=generate_3d_model,
    inputs=gr.Image(type="filepath"),
    outputs=[gr.Model3D(), gr.Textbox(label="Error Message", placeholder="")],
    title="$ECO 3D Creator",
    description="Upload an image to generate and view a 3D model.",
    css="""
        body, html {
            background-color: #000000; /* Black background */
            color: #FFFFFF; /* White text color for better visibility */
        }
        #logo {
            width: 100%; /* Full width */
            height: 100px; /* Fixed height */
            background: url('https://avatars.githubusercontent.com/u/194395535?s=48&v=4') no-repeat center center; 
            background-size: contain; /* Ensures that the logo will fit in the div */
            margin-bottom: 20px; /* Adds some space below the logo */
        }
        button { 
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
        }
        input[type='file'] {
            border: 2px dashed #4CAF50;
            display: block;
            width: 80%;
            padding: 15px;
            margin: 10px auto;
            box-sizing: border-box;
        }
        .gr-interface { /* Style the Gradio interface container */
            border-radius: 10px;
            border: 1px solid #333333; /* Subtle border */
        }
        .gr-output { /* Style for output components */
            background-color: #333333; /* Darker background for outputs */
            border: none;
        }
        .gr-input { /* Style for input components */
            background-color: #222222; /* Dark background for inputs */
            border: none;
        }
    """
)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))  # Default port or Render's provided port
    iface.launch(server_name="0.0.0.0", server_port=port)
