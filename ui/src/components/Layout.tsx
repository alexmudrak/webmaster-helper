import { faGithub } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { ReactNode } from 'react'

import NavBar from './NavBar'

interface LayoutProps {
  children: ReactNode
}

function Layout(props: LayoutProps) {
  return (
    <div>
      <NavBar />
      <div className='container my-2 shadow p-3 mb-5 bg-body rounded'>
        {props.children}
      </div>
      {/* Footer */}
      <footer className='footer mt-auto py-3 bg-light'>
        <div className='container text-center'>
          <a
            href='https://github.com/alexmudrak/webmaster-helper/'
            target='_blank'
            rel='noopener noreferrer'
          >
            <FontAwesomeIcon icon={faGithub} className='text-secondary' />
          </a>
          <span className='text-muted ms-2'>
            &copy; {new Date().getFullYear()} Webmaster Helper
          </span>
        </div>
      </footer>
    </div>
  )
}

export default Layout
