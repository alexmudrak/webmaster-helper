import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap'

import { useUserActions } from '../hooks/user.actions'

function NavBar() {
  const userActions = useUserActions()
  const handleLogout = () => {
    userActions.logout().catch((e) => {
      console.log('Logout problem')
    })
  }
  return (
    <Navbar collapseOnSelect expand='lg' className='bg-body-tertiary'>
      <Container>
        <Navbar.Brand href='#/'>Webmaster Helper</Navbar.Brand>
        <Navbar.Toggle aria-controls='basic-navbar-nav' />
        <Navbar.Collapse id='basic-navbar-nav' className='justify-content-end'>
          <Nav className='justify-content-end'>
            <Nav.Link href='#/webmasters'>Webmasters</Nav.Link>
            <Nav.Link href='#/contacts'>Contacts</Nav.Link>
            <Nav.Link href='#/projects'>Projects</Nav.Link>
            <Nav.Link href='#/payments'>Payments</Nav.Link>
            <NavDropdown title='Profile' id='basic-nav-dropdown'>
              <NavDropdown.Item href='#/profile-settings'>
                Settings
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item onClick={handleLogout}>
                Logout
              </NavDropdown.Item>
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default NavBar
