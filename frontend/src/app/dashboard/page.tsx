'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService, User } from '@/services/api';

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch {
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  const handleLogout = () => {
    authService.logout();
    router.push('/login');
  };

  if (!user) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow-sm rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            >
              Sair
            </button>
          </div>
          <div className="space-y-4">
            <p className="text-gray-600">
              Bem-vindo, <span className="font-semibold">{user.username}</span>!
            </p>
            <div className="border-t pt-4">
              <h2 className="text-lg text-black font-semibold mb-2">Seus dados:</h2>
              <p className="text-black">Email: {user.email}</p>
              <p className="text-black">Status: {user.is_active ? 'Ativo' : 'Inativo'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 