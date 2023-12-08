import React from 'react'

const NotFoundPage: React.FC = () => {
    return (
        <>
            <div className='container my-2 shadow p-3 mb-5 bg-body rounded'>
                <div className='mt-1 text-secondary text-center'>
                    <h2>404 - Page Not Found</h2>
                    <p>Sorry, the requested page does not exist.</p>
                </div>
            </div>
        </>
    )
}

export default NotFoundPage
