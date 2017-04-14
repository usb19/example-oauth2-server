# coding: utf-8

from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from playhouse.flask_utils import FlaskDB
from playhouse.shortcuts import model_to_dict

from playhouse.postgres_ext import DateTimeField, ForeignKeyField, TextField, PrimaryKeyField, IntegerField


DATABASE = {
    'name': 'headfirst',
    'engine': 'playhouse.pool.PooledPostgresqlExtDatabase',
    'register_hstore': False,
    'user': 'postgres',
    'host':'localhost',
    'password':'',
    'port':5432,
    'max_connections': 100,
    'stale_timeout': 6000,
}
app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'
app.config.from_object(__name__)

db = FlaskDB(app) 
oauth = OAuth2Provider(app)

class BaseModel(db.Model):
    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self._meta.get_field_names()])
    class Meta:
        schema = 'talentspear_auth'


'''
class UserProfile(BaseModel):
    aspiration              = TextField(db_column='ASPIRATION', null=True)
    currentCity             = TextField(db_column='CURRENT_CITY', null=True)
    fullName                = TextField(db_column='FULL_NAME', null=True)
    gender                  = TextField(db_column='GENDER', null=True)
    aadhaarNumber           = TextField(db_column='AADHAAR_NUMBER', null=True)
    mobileNumber            = TextField(db_column='MOBILE_NUMBER', null=True)
    webPresence             = JSONField(db_column='WEB_PRESENCE', null=True)
    profileId               = PrimaryKeyField(db_column='PROFILE_ID', sequence='profile_id_sequence')
    skills                  = JSONField(db_column='SKILLS', null=True)
    interest                = TextField(db_column='INTEREST', null=True)
    certificates            = TextField(db_column='CERTIFICATES', null=True)
    user                    = IntegerField(db_column='USER_ID')
    userDetails             = JSONField(db_column='USER_DETAILS', null=True)
    dateOfBirth             = DateTimeField(db_column='DATE_OF_BIRTH')
    projects                = JSONField(db_column='PROJECTS')
    
    class Meta:
        db_table = 'USER_PROFILE'

'''

class User(BaseModel):
    id = PrimaryKeyField(db_column = 'USER_ID', sequence='user_id_sequence')
    username =  TextField(db_column='USERNAME', null=True)
    
    class Meta:
        db_table='USER_TABLE'


class Client(BaseModel):
    client_id = TextField(db_column='CLIENT_ID', primary_key=True)
    client_secret = TextField(db_column='CLIENT_SECRET')
    user_id = ForeignKeyField(db_column = 'USER_ID', rel_model=User, to_field='id')
    _redirect_uris = TextField(db_column='REDIRECT_URIS')
    _default_scopes = TextField(db_column='DEFAULT_SCOPES')
    
        
    class Meta:
        db_table='CLIENT'
    
#     @property
#     def client_type(self):
#         return 'public'
# 
#     @property
#     def redirect_uris(self):
#         if self._redirect_uris:
#             return self._redirect_uris.split()
#         return []
# 
#     @property
#     def default_redirect_uri(self):
#         return self.redirect_uris[0]
# 
#     @property
#     def default_scopes(self):
#         if self._default_scopes:
#             return self._default_scopes.split()
#         return []


class Grant(BaseModel):
    grant_id = PrimaryKeyField(TextField,db_column = 'GRANT_ID')
    user_id = ForeignKeyField(db_column = 'USER_ID', rel_model=User, to_field='id')
    client_id = ForeignKeyField(db_column = 'CLIENT_ID', rel_model=Client, to_field='client_id')

    code = TextField(db_column='CODE', null=False)

    redirect_uri = TextField(db_column='REDIRECT_URI', null=True)
    expires = DateTimeField(db_column='EXPIRES', null=True)
    _scopes = TextField(db_column='SCOPES', null=True)
    
        
    class Meta:
        db_table='GRANT'

# 
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()
#         return self
# 
#     @property
#     def scopes(self):
#         if self._scopes:
#             return self._scopes.split()
#         return []


class Token(BaseModel):
    token_id = PrimaryKeyField(IntegerField,db_column = 'TOKEN_ID')
    user_id = ForeignKeyField(db_column = 'USER_ID', rel_model=User, to_field='id')
    client_id = ForeignKeyField(db_column = 'CLIENT_ID', rel_model=Client, to_field='client_id')

    # currently only bearer is supported
    token_type = TextField(db_column='TOKEN_TYPE')
    access_token = TextField(db_column='ACCESS_TOKEN')
    refresh_token = TextField(db_column='REFRESH_TOKEN')
    expires = DateTimeField(db_column='EXPIRES')
    _scopes = TextField(db_column='SCOPES')
    
        
    class Meta:
        db_table='TOKEN'

# 
#     @property
#     def scopes(self):
#         if self._scopes:
#             return self._scopes.split()
#         return []


def current_user():
    if 'id' in session:
        uid = session['id']
        try:
            return User.select().where(User.id == uid).get()
        except Exception:
            return None
    return None

@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        try:
            user = User.select().where(User.username == username).get()
            session['id'] = user.id
            return render_template('home.html', user=user)
        except Exception:
            user = User.create(username=username)
            session['id'] = user.id
            return render_template('home.html', user=user)
    if request.method == 'GET':
        return render_template('home.html', user=current_user())


@app.route('/clients')
def client_function():
    user = current_user()
    if not user:
        return redirect('/')
    try:
        res = Client.select().where(Client.user_id == user.id).get()
        return jsonify(
        client_id=res.client_id,
           client_secret=res.client_secret
           )  
#         res = Client.update(client_secret=gen_salt(50)).where(Client.user_id.id==user.id)
#         print model_to_dict(res)
    except Exception:
        item = Client.create(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris= 'http://localhost:8000/authorized',
        _default_scopes='email',
        user_id=user.id
        )
        re = model_to_dict(item)
        res = Client.select().where(Client.client_id==re.get('client_id')).get()
        return jsonify(
        client_id=res.client_id,
           client_secret=res.client_secret
           )  

@oauth.clientgetter
def load_client(client_id):
    return Client.select().where(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.select().where(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    result = Grant.create(grant)
    return result


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.select().where(access_token=access_token).first()
    elif refresh_token:
        return Token.select().where(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    Token.delete().where(
        client_id=request.client.client_id,
        user_id=request.user.id
    ).execute
    # make sure that every client has only one token connected to a user
#     for t in toks:
#         db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token.create(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    return tok


@app.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    try:
        user = current_user()
    except Exception:
        return redirect('/')
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@app.route('/api/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)


if __name__ == '__main__':
    app.run()
