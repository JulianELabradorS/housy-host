# Housy-host

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages.

```bash
pip install -r requirements.txt
```

Add Firebase credentials file to `/assets` with the name firebase-credentials.json
![imagen](https://user-images.githubusercontent.com/31170000/218464356-d864fba8-316d-47a3-9a21-282d3314ff5f.png)


## Usage

Execute the reservations controller file

```bash
python reservations_controller.py
```
That will start the server running with ngrok and assign you an url address to use publicly.

![imagen](https://user-images.githubusercontent.com/31170000/218459526-887ed326-593b-4436-8da9-4753bcd2d258.png)

### Initial load of reservations in Firebase
Endpoint to save all reservations from Hostaway to Firebase. You have to make a request to /load-reservations endpoint.
>This will take ~15 minutes

![imagen](https://user-images.githubusercontent.com/31170000/218461581-7acdf17a-3097-4687-80ab-4c425a99baf3.png)


### Webhook that updates the reservations data
You have to add that .ngrok.io address to the [Unified webhook](https://dashboard.hostaway.com/settings/integrations) in Hostaway dashboard.
> The added url in hostaway dashboard should be pointing to /unified-webhook endpoint. Example: http://31fc-181-165-197-31.ngrok.io/unified-webhook

![imagen](https://user-images.githubusercontent.com/31170000/218460310-87994e19-be82-4dbc-9376-82a414b30545.png)
