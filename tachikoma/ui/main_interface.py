"""
Main Gradio interface for Tachikoma.

This module contains the main user interface for the Tachikoma system.
"""

import gradio as gr
from typing import Any


class TachikomaInterface:
    """Main interface for the Tachikoma system."""

    def __init__(self, orchestrator: Any):
        """Initialize the interface."""
        self.orchestrator = orchestrator
        self.interface = None

    def create_interface(self) -> gr.Blocks:
        """Create the main Gradio interface."""
        with gr.Blocks(title="Tachikoma Multi-Agent AI System") as interface:
            gr.Markdown("# Tachikoma Multi-Agent AI System")
            gr.Markdown(
                "Dynamic, character-driven agents that collaborate while maintaining their ground."
            )

            # Placeholder interface
            with gr.Row():
                task_input = gr.Textbox(label="Enter your task", lines=3)
                prefs_input = gr.Textbox(label="Preferences", lines=3)

            with gr.Row():
                run_btn = gr.Button("Run", variant="primary")
                # pause_btn = gr.Button("Pause")  # Will be used in future implementation
                # cont_btn = gr.Button("Continue")  # Will be used in future implementation

            status_display = gr.Markdown("Status: Ready")
            output_display = gr.Textbox(label="Output", lines=10)

            # Placeholder event handlers
            def run_task(task, prefs):
                return "Task processing placeholder", "Status: Processing..."

            run_btn.click(
                run_task, [task_input, prefs_input], [output_display, status_display]
            )

        self.interface = interface
        return interface

    async def launch(self):
        """Launch the interface."""
        if self.interface is None:
            self.create_interface()

        # Launch the interface
        self.interface.queue().launch()
