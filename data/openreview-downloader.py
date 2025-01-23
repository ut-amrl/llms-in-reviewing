import openreview
import os

def get_openreview_credentials():
    # First check if the credentials are in the .openreview_credentials file
    credentials_file = ".openreview_credentials"
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as file:
            lines = file.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
            return username, password

    # If not found, prompt the user to enter the credentials
    username = input("Enter your OpenReview username: ")
    password = input("Enter your OpenReview password: ")
    return username, password

def main():
    # API V2
    username, password = get_openreview_credentials()
    client = openreview.api.OpenReviewClient(
        baseurl='https://api2.openreview.net',
        username=username,
        password=password
    )
    venue_id = 'ICLR.cc/2024'
    venue_group = client.get_group(venue_id)
    submission_name = venue_group.content['submission_name']['value']
    submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')

if __name__ == "__main__":
    main()


client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username=username,
    password=password
)
venue_id = 'ICLR.cc/2024'
venue_group = client.get_group(venue_id)
submission_name = venue_group.content['submission_name']['value']
submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}', details='replies')
