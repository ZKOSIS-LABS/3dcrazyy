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
            position: fixed; /* Fixed position */
            left: 0; /* Left alignment */
            top: 0; /* Top alignment */
            height: 100px; /* Fixed height */
            background: url('/logo.png') no-repeat center center; 
            background-size: contain; /* Ensures that the logo will fit in the div */
            margin-bottom: 20px; /* Adds some space below the logo */
        }
        footer {
        display:none;
        opacity:0;
        }
    """
)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))  # Default port or Render's provided port
    iface.launch(server_name="0.0.0.0", server_port=port)
