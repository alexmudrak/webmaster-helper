import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

import App from './App'

describe('App', () => {
  it('Check App', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )

    await waitFor(() => screen.getByText('Loading...'), { timeout: 5000 })
  })
})
