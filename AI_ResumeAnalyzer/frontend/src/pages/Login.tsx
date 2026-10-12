import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { LogIn } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(''); setLoading(true);
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    try {
      const res = await axios.post('http://localhost:8000/api/auth/login', formData);
      login(res.data.access_token, res.data.user);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-[#F8F7FC] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="mx-auto w-12 h-12 rounded-lg bg-violet-600 text-white flex items-center justify-center font-bold text-2xl shadow-sm mb-4">R</div>
        <h2 className="text-3xl font-bold text-[#18181B]">Welcome back</h2>
        <p className="mt-2 text-sm text-[#71717A]">Sign in to your ResumeAI account</p>
      </div>
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-sm border border-[#E4E4E7] sm:rounded-xl sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && <div className="p-3 bg-red-50 text-red-600 text-sm rounded-md border border-red-200">{error}</div>}
            <div>
              <label className="block text-sm font-medium text-[#3F3F46]">Email address</label>
              <input type="email" required value={email} onChange={e => setEmail(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-[#E4E4E7] rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-violet-500 focus:border-violet-500 sm:text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-[#3F3F46]">Password</label>
              <input type="password" required value={password} onChange={e => setPassword(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-[#E4E4E7] rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-violet-500 focus:border-violet-500 sm:text-sm" />
            </div>
            <button type="submit" disabled={loading}
              className="w-full flex justify-center items-center gap-2 py-2.5 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-violet-600 hover:bg-violet-700 focus:outline-none disabled:bg-violet-300 transition-colors">
              {loading ? 'Signing in...' : <><LogIn size={16} /> Sign in</>}
            </button>
          </form>
          <div className="mt-6 text-center">
            <p className="text-sm text-[#71717A]">Don't have an account? <Link to="/register" className="font-medium text-violet-600 hover:text-violet-500">Create one</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
}