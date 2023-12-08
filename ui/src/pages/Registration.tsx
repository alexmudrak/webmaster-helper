import RegistrationForm from '../components/auth/RegistrationForm';
import { getUser } from '../hooks/user.actions';
import { Navigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Registration() {
  const user = getUser();

  return (
    <div className='container d-flex justify-content-center align-items-center vh-100'>
      <div className='card p-4 shadow'>
        {user ? (
          <Navigate to='/' />
        ) : (
          <>
            <h2 className='text-center mb-4'>Register</h2>
            <RegistrationForm />
            <div className='mt-3 text-center text-secondary'>
              Already have an account? <Link to='/login/'>Login here</Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default Registration;
