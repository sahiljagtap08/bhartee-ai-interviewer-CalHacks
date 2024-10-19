import random
import reflex as rx

from rxconfig import config
from reflex.components.radix.themes.base import LiteralAccentColor

# Skills data
skills = [
    "Data Management",
    "Networking",
    "Security",
    "Cloud",
    "DevOps",
    "Data Science",
    "AI",
    "ML",
    "Robotics",
    "Cybersecurity",
]

# Chip properties
chip_props = {
    "radius": "full",
    "variant": "surface",
    "size": "3",
    "cursor": "pointer",
    "style": {"_hover": {"opacity": 0.75}},
}

class State(rx.State):
    """The app state."""

    # Selected skills
    selected_items: list[str] = skills[:3]

    def add_selected(self, item: str):
        if item not in self.selected_items:
            self.selected_items.append(item)

    def remove_selected(self, item: str):
        if item in self.selected_items:
            self.selected_items.remove(item)

    def add_all_selected(self):
        self.selected_items = list(skills)

    def clear_selected(self):
        self.selected_items.clear()

    def random_selected(self):
        self.selected_items = random.sample(
            skills, k=random.randint(1, len(skills))
        )

def action_button(
    icon: str,
    label: str,
    on_click: callable,
    color_scheme: LiteralAccentColor,
) -> rx.Component:
    return rx.button(
        rx.icon(icon, size=16),
        label,
        variant="soft",
        size="2",
        on_click=on_click,
        color_scheme=color_scheme,
        cursor="pointer",
    )

def selected_item_chip(item: str) -> rx.Component:
    return rx.badge(
        item,
        rx.icon("circle-x", size=18),
        color_scheme="green",
        **chip_props,
        on_click=lambda: State.remove_selected(item),
    )

def unselected_item_chip(item: str) -> rx.Component:
    return rx.cond(
        State.selected_items.contains(item),
        rx.fragment(),
        rx.badge(
            item,
            rx.icon("circle-plus", size=18),
            color_scheme="gray",
            **chip_props,
            on_click=lambda: State.add_selected(item),
        ),
    )

def items_selector() -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.hstack(
                rx.icon("lightbulb", size=20),
                rx.heading(
                    "Area of Focus"
                    + f" ({State.selected_items.length()})",
                    size="4",
                ),
                spacing="1",
                align="center",
                width="100%",
                justify_content=["end", "start"],
            ),
            rx.hstack(
                action_button(
                    "plus",
                    "Add All",
                    State.add_all_selected,
                    "green",
                ),
                action_button(
                    "trash",
                    "Clear All",
                    State.clear_selected,
                    "tomato",
                ),
                action_button(
                    "shuffle",
                    "",
                    State.random_selected,
                    "gray",
                ),
                spacing="2",
                justify="end",
                width="100%",
            ),
            justify="between",
            flex_direction=["column", "row"],
            align="center",
            spacing="2",
            margin_bottom="10px",
            width="100%",
        ),
        # Selected Items
        rx.flex(
            rx.foreach(
                State.selected_items,
                selected_item_chip,
            ),
            wrap="wrap",
            spacing="2",
            justify_content="start",
        ),
        rx.divider(),
        # Unselected Items
        rx.flex(
            rx.foreach(skills, unselected_item_chip),
            wrap="wrap",
            spacing="2",
            justify_content="start",
        ),
        justify_content="start",
        align_items="start",
        width="100%",
    )

def form_field(
    label: str, placeholder: str, type: str, name: str
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.form.label(label),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )

def contact_form() -> rx.Component:
    def handle_submit(form_data):
        """Handle form submission."""
        # Show alert
        rx.window_alert(f"Form Submitted: {form_data.to_string()}")
        # Redirect after submission
        return rx.redirect("/interview_page")

    return rx.card(
        rx.flex(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="user", size=32),
                    color_scheme="green",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.heading(
                        "Provide Us Your Information",
                        size="4",
                        weight="bold",
                    ),
                    rx.text(
                        "Fill the form so we can contact you and provide you a seamless interview process.",
                        size="2",
                    ),
                    spacing="1",
                    height="100%",
                ),
                spacing="4",
                align_items="center",
                width="100%",
            ),
            rx.form.root(
                rx.flex(
                    # Personal Information Section
                    rx.flex(
                        form_field(
                            "First Name",
                            "First Name",
                            "text",
                            "first_name",
                        ),
                        form_field(
                            "Last Name",
                            "Last Name",
                            "text",
                            "last_name",
                        ),
                        spacing="3",
                        flex_direction=["column", "row", "row"],
                    ),
                    rx.flex(
                        form_field(
                            "Email",
                            "user@example.com",
                            "email",
                            "email",
                        ),
                        form_field(
                            "Phone", "Phone", "tel", "phone"
                        ),
                        spacing="3",
                        flex_direction=["column", "row", "row"],
                    ),
                    # Technical Skills Section
                    rx.box(
                        rx.text(
                            "Technical Skills",
                            style={
                                "font-size": "18px",
                                "font-weight": "600",
                                "margin-top": "20px",
                            },
                        ),
                        items_selector(),
                    ),
                    # Message Section
                    rx.flex(
                        rx.text(
                            "Other Info",
                            style={
                                "font-size": "15px",
                                "font-weight": "500",
                                "line-height": "35px",
                            },
                        ),
                        rx.text_area(
                            placeholder="Message",
                            name="message",
                            resize="vertical",
                        ),
                        direction="column",
                        spacing="1",
                    ),
                    # Submit Button
                    rx.form.submit(
                        rx.button("Submit and Start Interview", type="submit", size="lg"),
                        as_child=True,
                    ),
                    direction="column",
                    spacing="4",
                    width="100%",
                ),
                # Use handle_submit to display alert and redirect
                on_submit=handle_submit,
                reset_on_submit=False,
            ),
            width="100%",
            direction="column",
            spacing="4",
        ),
        size="3",
    )


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="absolute", top="1rem", right="1rem"),
        rx.heading(
            "Bhartee AI",
            size="9",
            text_align="center",
            position="absolute",
            top="1rem",
            left="50%",
            transform="translateX(-50%)",
        ),
        rx.vstack(
            rx.text(
                "Welcome! Please complete the form below to apply for a technical interview with us.",
                size="5",
                text_align="center",
            ),
            contact_form(),
            spacing="4",
            align_items="center",
            justify_content="center",
            min_height="80vh",
            margin_top="50px",  # Added this line to move the form down
        ),
        position="relative",
        height="100vh",
    )

class FormCheckboxState(rx.State):
    """Handle the state of the consent form."""
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        """Handle the form submit and navigate to interview page."""
        self.form_data = form_data
        if form_data.get("checkbox", False):
            return rx.redirect("/interview_process")
        else:
            rx.window_alert("You must accept the terms to proceed.")


def consent_form() -> rx.Component:
    """The consent form component."""
    return rx.card(
        rx.vstack(
            rx.heading("Job Interview Consent Form", size="4", text_align="center", margin_bottom="1rem"),
            # Adding the formatted consent text with line breaks and indentation for readability
            rx.text(
                (
                    "I voluntarily agree to participate in this job interview process.\n\n"
                    "- I understand that my participation is voluntary, and I can withdraw at any time or refuse to answer any questions without any negative consequences.\n"
                    "- I understand that I can withdraw permission to use the data from my interview within two weeks after the interview, in which case the material will be deleted.\n"
                    "- I have had the purpose and nature of the interview process explained to me in writing, and I have had the opportunity to ask any questions I may have.\n"
                    "- I understand that participation in this process involves only voice recording of the interview.\n"
                    "- I understand that I will not benefit directly from participating in this interview process.\n"
                    "- I agree to my interview being audio-recorded.\n"
                    "- I understand that all information I provide during the interview will be treated confidentially.\n"
                    "- I understand that in any report or notes made from this interview, identifying details will be removed to maintain anonymity.\n"
                    "- I understand that the audio recording of my interview will be stored securely and accessible only to authorized personnel.\n"
                    "- I understand that the audio recording will be retained until the hiring decision is made or for a set period afterward.\n"
                    "- I understand that I can request access to my interview data under relevant freedom of information legislation while it is in storage.\n"
                    "- I am free to contact the interview coordinator or other relevant personnel for further information.\n"
                ),
                text_align="justify",  # Justified text for better alignment
                white_space="pre-line",  # Keep line breaks intact
                line_height="1.8",  # Further increase line height for readability
                padding="2rem",  # Add more padding to the text
                font_size="1.1rem",  # Increase font size for readability
            ),
            rx.form.root(
                rx.hstack(
                    rx.checkbox(
                        name="checkbox",
                        label="I accept the terms and conditions",
                        size="lg",
                    ),
                    rx.button("Submit", type="submit", size="lg"),
                    justify="space-between",
                    width="100%",
                ),
                on_submit=FormCheckboxState.handle_submit,
                reset_on_submit=False,
            ),
            width="100%",
            padding="2rem",
        ),
        width=["100%", "100%", "100%"],  # Make the box wider for different screen sizes
        max_width="1200px",  # Maximum width to prevent it from becoming too wide on large screens
        margin="auto",  # Center the card
        margin_top="4rem",  # Slightly reduce top margin for balance
        padding="3rem",  # Increase the padding for more space around the content
        box_shadow="xl",  # Add a larger shadow for a more pronounced effect
        border_radius="lg",  # Further round the corners
        background_color="black",  # Ensure it stands out
        color="white",  # Ensure text is readable against the black background
    )



def interview_page() -> rx.Component:
    """The interview consent page."""
    return rx.container(
        rx.heading(
            "Consent Form",
            size="9",
            text_align="center",
            margin_top="50px",
        ),
        consent_form(),
        position="relative",
        height="100vh",
    )


def interview_process_page() -> rx.Component:
    """The actual interview page component."""
    return rx.container(
        rx.heading(
            "Interview Process",
            size="9",
            text_align="center",
            margin_top="50px",
        ),
        rx.text(
            "This is where the actual interview will take place.",
            size="5",
            text_align="center",
            margin_top="20px",
        ),
        rx.link(
            rx.button("Back to Home"),
            href="/",
            position="absolute",
            top="1rem",
            left="1rem",
        ),
        position="relative",
        height="100vh",
    )


app = rx.App()
app.add_page(index, route="/")                       # Existing main page
app.add_page(interview_page, route="/interview_page") # Consent page
app.add_page(interview_process_page, route="/interview_process")  # Actual interview page
app._compile()
