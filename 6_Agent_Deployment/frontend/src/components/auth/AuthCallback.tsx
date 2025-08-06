import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '@/lib/supabase';
import { Loader } from 'lucide-react';

/**
 * Component to handle OAuth callback redirects
 * This component processes the OAuth callback from providers like Google
 */
export const AuthCallback = () => {
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Process the OAuth callback
    const handleAuthCallback = async () => {
      try {
        console.log('AuthCallback: Processing callback at URL:', window.location.href);
        
        // Get the auth code from the URL
        const hashParams = new URLSearchParams(window.location.hash.substring(1));
        const queryParams = new URLSearchParams(window.location.search);
        
        console.log('AuthCallback: Hash params:', Object.fromEntries(hashParams));
        console.log('AuthCallback: Query params:', Object.fromEntries(queryParams));
        
        // If there's an error in the URL, display it
        const errorParam = hashParams.get('error') || queryParams.get('error');
        if (errorParam) {
          console.log('AuthCallback: Error found:', errorParam);
          setError(errorParam);
          return;
        }

        // Exchange the auth code for a session
        const { data, error } = await supabase.auth.getSession();
        
        console.log('AuthCallback: Session data:', data);
        console.log('AuthCallback: Session error:', error);
        
        if (error) {
          throw error;
        }

        if (data?.session) {
          console.log('AuthCallback: Session found, redirecting to home');
          // Successfully authenticated, redirect to home
          navigate('/');
        } else {
          console.log('AuthCallback: No session found, redirecting to login');
          // No session found, redirect to login
          navigate('/login');
        }
      } catch (err) {
        console.error('Error during auth callback:', err);
        setError('Authentication failed. Please try again.');
      }
    };

    handleAuthCallback();
  }, [navigate]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      {error ? (
        <div className="text-center">
          <h2 className="text-xl font-semibold text-red-500 mb-2">Authentication Error</h2>
          <p className="text-gray-600 dark:text-gray-400">{error}</p>
          <button 
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            onClick={() => navigate('/login')}
          >
            Return to Login
          </button>
        </div>
      ) : (
        <div className="text-center">
          <Loader className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-500" />
          <p className="text-gray-600 dark:text-gray-400">Completing authentication...</p>
        </div>
      )}
    </div>
  );
};

export default AuthCallback;
