import 'bootstrap/dist/css/bootstrap.min.css';
import './globals.css';
import { AuthProvider } from '../context/AuthContext';

export const metadata = {
  title: 'AI Chatbot',
  description: 'Django-based AI Chatbot',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
