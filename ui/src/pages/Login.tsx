import LoginForm from '../components/auth/LoginForm';
import { getUser } from '../hooks/user.actions';
import { Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Login() {
  const user = getUser();

  return (
    <div className='container d-flex justify-content-center align-items-center vh-100'>
      <div className='card p-4 shadow'>
        {user ? (
          <Navigate to='/' />
        ) : (
          <>
            <h2 className='text-center mb-4'>Login</h2>
            <LoginForm />
            <div className='mt-3 text-center text-secondary'>
              Don't have an account? <Link to='/registration/'>Register here</Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Login;
