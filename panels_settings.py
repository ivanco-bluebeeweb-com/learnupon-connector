"""Settings panel for LearnUpon Connector."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

@ext.panel("__learnupon_settings", slot="center")
async def settings_panel(ctx) -> ui.UINode:
    disconnect_form = ui.Form(
        # id=learnupon_form",
        submit_label="Disconnect Active Account",
        action=ui.Call("disconnect_learnupon"),
        children=[
            ui.Input(param_name="connection_id", placeholder="e.g. conn_123")
        ]
    )

    return ui.Stack(
        children=[
            ui.Heading("LearnUpon Settings & Accounts", level=2),
            ui.Text("Manage connected credentials and review health metrics.", variant="body"),
            ui.Divider(),
            ui.Button(
                "Run Health Audit",
                variant="primary",
                on_click=ui.Call("audit_health")
            ),
            ui.Divider(),
            ui.Heading("Disconnect Account", level=3),
            ui.Text("Removing the connection permanently wipes saved API tokens from secure storage.", variant="caption"),
            disconnect_form
        ]
    )
