import numpy as np
from scipy.integrate import quad
import gradio as gr

def r(z, h, bL, bK):
    return (bK / 2) + ((bL - bK) / 2) * (1 - ((2 * z / h - 1) ** 2))

def segment_area(f, r_val):
    if f <= 0:
        return 0
    if f >= 2 * r_val:
        return np.pi * r_val**2
    try:
        return r_val**2 * np.arccos((r_val - f) / r_val) - (r_val - f) * np.sqrt(2 * r_val * f - f**2)
    except ValueError:
        return 0

def volume(f, h, bL, bK):
    integrand = lambda z: segment_area(f, r(z, h, bL, bK))
    vol, _ = quad(integrand, 0, h)
    return f"Volumen: {1000* vol:.4f} l"

# Gradio-Interface
interface = gr.Interface(
    fn=volume,
    inputs=[
        gr.Number(label="Füllhöhe f (m)", value=0.5),
        gr.Number(label="Fasslänge h (m)", value=1.0),
        gr.Number(label="Durchmesser Mitte bL (m)", value=0.9),
        gr.Number(label="Durchmesser Rand bK (m)", value=0.8)
    ],
    outputs="text",
    title="Fass-Volumenrechner",
    description="Berechnet das Volumen eines liegenden, bauchigen Fasses anhand der Füllhöhe und Maße."
)

interface.launch()
