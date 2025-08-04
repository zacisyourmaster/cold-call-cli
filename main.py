from jinja2 import Template
import yaml
# import smtplib
# import argparse
# import os

CONFIG_PATH = "config.yml"


def load_config():
    """Load user data from config file"""
    try:
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Config not found at {CONFIG_PATH}")
        print("Please create a config file with your details:")
        print(
            """
        user:
          name: "Your Name"
          email: "your@email.com"
          phone: 12345678910
          experience: "blah blah blah"
        """
        )
        exit(1)


def load_template(template_name):
    path = f"templates/{template_name}.txt"
    with open(path, "r") as f:
        data = f.read()
    return data.split('---')


def render_email(template_name, context):
    raw_subject, raw_body = load_template(template_name)
    subject = Template(raw_subject).render(**context)
    body = Template(raw_body).render(**context)
    return subject, body

def save_email(subject,body, name, company):
    with open(f"outbox/temp_{name}_{company}", "w") as f:
        f.write(subject+'\n---\n'+body)
        
# def send_email(recipient, subject, body):
#     pass


def get_user_input() -> dict:
    print("Please enter the following info:\n")
    return {
        "recipient_name": input("Recipient First Name: ").strip(),
        "recipient_email": input("Recipient Email: ").strip(),
        "company": input("Company Name: ").strip(),
        "job_title": input("Job Title: ").strip(),
        "template_name": input("Template Name: ").strip()
    }


def main():
    config = load_config()
    user_data = config["user"]

    user_input = get_user_input()
    context = {**user_data, **user_input}
    
    subject,body=render_email(user_input["template_name"],context)
    
    print("Subject:")
    print(subject)
    print("Body:")
    print(body)
    save_email(subject,body,user_input["recipient_name"],user_input["company"])
    # parser = argparse.ArgumentParser(description="Render and optionally send a cold email.")
    # parser.add_argument("--template", required=True, help="Name of the email template (without .yaml)")
    # parser.add_argument("--recipient", required=True, help="Email address of the recipient")
    # parser.add_argument("--first_name", required=True, help="Recipient's first name")
    # parser.add_argument("--your_name", required=True, help="Your full name")
    # parser.add_argument("--role", required=True, help="Your current/previous role")
    # parser.add_argument("--years_experience", required=True, help="Years of experience")
    # parser.add_argument("--industries", required=True, help="Industries or niches you've specialized in")
    # parser.add_argument("--achievement", required=True, help="A noteworthy achievement")
    # parser.add_argument("--target_role", required=True, help="Job title you're applying for")
    # parser.add_argument("--recent_activity", required=True, help="Something the team is working on")
    # parser.add_argument("--send", action="store_true", help="Actually send the email after rendering (not implemented yet)")

    # args = parser.parse_args()
    # context = vars(args)

    # subject, body = render_email(args.template, context)

    # print("\n--- Email Preview ---")
    # print(f"To: {args.recipient}")
    # print(f"Subject: {subject}\n")
    # print(body)

    # if args.send:
    #     print("\n(Send functionality not implemented yet)")
    # else:
    #     print("\nEmail not sent. Use --send to enable sending.")


if __name__ == "__main__":
    main()
