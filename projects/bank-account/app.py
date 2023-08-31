import pyotp
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, callback_context, no_update

from account_manager import AccountManager

account_manager = AccountManager()

# Define the background image URL
background_image_url = "assets/background-image.jpg"
external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', 
    'https://use.fontawesome.com/releases/v5.15.1/css/all.css'
]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = 'Bank App'

def render_login_layout():
    login_layout = html.Div([
        html.Div(className='container', children=[
            html.H1("Login", className='mt-5'),
            dcc.Input(id='account-number', type='text', placeholder='Account Number', className='form-control mb-3'),
            dcc.Input(id='pin', type='password', placeholder='PIN', className='form-control mb-3'),
            html.Div([
                html.Button([html.I(className='fas fa-sign-in-alt'), ' Login'], id='login-button', className='btn btn-info flex-fill'),
                html.Button([html.I(className='fas fa-user-plus'), ' Add Account'], id='add-account-button', className='btn btn-success flex-fill ml-2'),
            ], style={'display': 'flex', 'gap': '10px'})
        ])
    ])
    
    return login_layout

def render_home_layout(account_number):
    home_layout = html.Div([
        html.Div(className='container', children=[
            html.H1(f"Welcome to Your Account - A/C: {account_number}", className='mt-5'),
            dcc.Input(id='amount', type='number', placeholder='Enter Amount', className='form-control mb-3'),
            html.Button([html.I(className='fas fa-dollar-sign'), ' Check Balance'], id='balance-button', className='btn btn-info'),
            html.Button([html.I(className='fas fa-money-bill-wave'), ' Withdraw Money'], id='withdraw-button', className='btn btn-danger mr-1 ml-1'),
            html.Button([html.I(className='fas fa-coins'), ' Deposit Money'], id='deposit-button', className='btn btn-success mr-2'),
            html.Button([html.I(className='fas fa-sign-out-alt'), ' Logout'], id='logout-button', className='btn btn-secondary'),
            html.Div(id='result', className='mt-3')
        ])
    ])
    
    return home_layout


# Create a TOTP instance with a shared secret
shared_secret = pyotp.random_base32()
totp = pyotp.TOTP(shared_secret)

def generate_otp():
    return totp.now()

def render_add_account_layout():
    
    otp = generate_otp()
    
    add_account_layout = html.Div([
        html.Div(className='container', children=[
            html.H1("Add Account", className='mt-5'),
            dcc.Input(id='new-account-number', type='text', placeholder='New Account Number', className='form-control mb-3'),
            dcc.Input(id='new-pin', type='password', placeholder='New PIN', className='form-control mb-3'),
            dcc.Input(id='confirm-new-pin', type='password', placeholder='Confirm New PIN', className='form-control mb-3'),
            dcc.Input(id='otp', type='text', value=otp, placeholder='OTP', className='form-control mb-3'),
            html.Div([
                html.Button([html.I(className='fas fa-user-plus'), ' Add Account'], id='add-new-account-button', className='btn btn-success mr-2'),
                html.Button([html.I(className='fas fa-arrow-left'), ' Back to Login'], id='back-to-login-button', className='btn btn-secondary')
            ], style={'display': 'flex', 'gap': '10px'}),
            html.Div(id='result-add-account', className='mt-3')
        ])
    ])
    
    return add_account_layout

app.layout = dbc.Container(
    style={
        'background-image': f'url("{background_image_url}")',
        'background-size': 'cover',
        'background-repeat': 'no-repeat',
        'background-position': 'center center',
        'position': 'fixed',  # Fix the background in place
        'top': 0, 'right': 0, 'bottom': 0, 'left': 0,  # Cover the entire viewport
        'z-index': '-1',  # Place the background behind the content
    },
    fluid=True,
    children=[
        dcc.Store(id='account-store'),
        dcc.Location(id='url', refresh=False),
        dbc.Container(id='page-content')
    ]
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    Input('account-store', 'data')
)
def display_page(pathname, account_number):
    
    if pathname == '/':
        return render_login_layout()
    elif pathname == '/home':
        return render_home_layout(account_number)
    elif pathname == '/add-account':
        return render_add_account_layout()
    else:
        return "404 Page not found"


@app.callback(
    Output('account-store', 'data'),
    Output('url', 'pathname'),
    Input('login-button', 'n_clicks'),
    Input('add-account-button', 'n_clicks'),
    State('account-number', 'value'),
    State('pin', 'value')
)
def login(login_clicks, add_account_clicks, account_number, pin):
    
    ctx = callback_context 
    if not ctx.triggered:
        return no_update, no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'login-button':
        if account_manager.authenticate(account_number, pin):
            return account_number, '/home'
    elif trigger_id == 'add-account-button':
        return no_update, '/add-account'

    return no_update, no_update

@app.callback(
    Output('result-add-account', 'children'),
    Input('add-new-account-button', 'n_clicks'),
    Input('back-to-login-button', 'n_clicks'),
    State('new-account-number', 'value'),
    State('new-pin', 'value'),
    State('confirm-new-pin', 'value'),
    State('otp', 'value')
)
def add_account(add_account_clicks, back_clicks, new_account_number, new_pin, confirm_new_pin, otp):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'add-new-account-button':
        return dcc.Location(pathname='/', id='button-add-new-account')
    elif button_id == 'back-to-login-button':
        return dcc.Location(pathname='/', id='back-button-to-login')
    else:
        return no_update

@app.callback(
    Output('result', 'children'),
    Input('balance-button', 'n_clicks'),
    Input('withdraw-button', 'n_clicks'),
    Input('deposit-button', 'n_clicks'),
    Input('logout-button', 'n_clicks'),
    State('amount', 'value'),
    Input('back-to-login-button', 'n_clicks')
)
def perform_action(balance_clicks, withdraw_clicks, deposit_clicks, logout_clicks, amount):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'balance-button':
        result = account_manager.check_balance()
    elif button_id == 'withdraw-button':
        result = account_manager.withdraw_money(
            money_to_withdraw=int(amount) if amount != None else 0
        )
    elif button_id == 'deposit-button':
        result = account_manager.deposit_money(
            money_to_deposit=int(amount) if amount != None else 0
        )
    elif button_id == 'logout-button':
        return dcc.Location(pathname='/', id='logout-redirect')
    else:
        result = ""

    return html.Div(result)



if __name__ == '__main__':
    app.run_server(debug=True)
