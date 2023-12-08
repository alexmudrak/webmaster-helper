import { Navigate } from 'react-router-dom'
import { getUser } from '../hooks/user.actions'
import { ReactComponent } from '../types'
import Layout from '../components/Layout'

function ProtectedRoute({ children }: ReactComponent) {
    const user = getUser()
    return user ? <Layout>{children}</Layout> : <Navigate to='/login/' />
}

export default ProtectedRoute
