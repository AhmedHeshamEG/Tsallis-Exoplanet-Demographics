import gradio as gr
import numpy as np

# --- Our Discovered Parameters ---
Q_INDEX = 1.8591
KAPPA = 0.2121
A_MET = 1.0789
ALPHA_MASS = 0.9825
BETA_MASS = 2.2413

def calculate_exoplanet_probability(stellar_mass, metallicity):
    """
    The mathematical core of our paper.
    Takes Mass (M) and Metallicity (Z) and returns a percentage.
    """
    M = float(stellar_mass)
    Z = float(metallicity)
    
    # Calculate the Stellar Potential (Phi)
    # Phi = kappa * 10^(a*Z) * M^alpha * exp(-beta*M)
    Z_term = np.power(10.0, A_MET * Z)
    M_term = np.power(max(M, 1e-5), ALPHA_MASS) * np.exp(-BETA_MASS * M)
    Phi = KAPPA * Z_term * M_term
    
    # The Tsallis q-exponential
    base = 1.0 - (1.0 - Q_INDEX) * Phi
    
    if base <= 0:
        base = 0.0
        
    eq_minus_Phi = np.power(base, 1.0 / (1.0 - Q_INDEX))
    
    # Final Probability
    P = 1.0 - eq_minus_Phi
    
    # Convert to a friendly percentage string
    P_percent = P * 100
    
    # Format the output 
    return f"{P_percent:.2f}%"

# --- The User Interface (Gradio) ---
# We wrap our math in a beautiful web page
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# Exoplanet Probability Calculator")
    gr.Markdown("### Based on the Tsallis Non-Extensive Statistical Mechanics Framework")
    gr.Markdown(
        "Adjust the properties of a hypothetical star below. Our phenomenological model, "
        "trained on 197,000 stars from the Kepler DR25 catalog, will calculate the probability "
        "that it hosts a detectable exoplanetary system."
    )
    
    with gr.Row():
        with gr.Column():
            # Input Sliders bounded by our real data limits
            mass_slider = gr.Slider(
                minimum=0.1, maximum=2.5, step=0.05, value=1.0, 
                label="Stellar Mass (Solar Masses)",
                info="1.0 is equal to our Sun. >1.5 are hot, massive stars."
            )
            metal_slider = gr.Slider(
                minimum=-1.0, maximum=0.5, step=0.05, value=0.0, 
                label="Metallicity [Fe/H]",
                info="0.0 is Solar metallicity. Negative means metal-poor."
            )
            
            calc_button = gr.Button("Calculate Probability", variant="primary")
            
        with gr.Column():
            # Output Display
            output_text = gr.Text(
                label="Probability of Hosting an Exoplanet", 
                value="Waiting for input..."
            )
            
    # Connect the button to our math function
    calc_button.click(
        fn=calculate_exoplanet_probability, 
        inputs=[mass_slider, metal_slider], 
        outputs=output_text
    )
    
    gr.Markdown("---")
    gr.Markdown("*Developed by Ahmed Hesham for arXiv Publication.*")

# Start the web server
if __name__ == "__main__":
    demo.launch()