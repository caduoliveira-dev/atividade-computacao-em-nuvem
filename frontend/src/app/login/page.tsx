import LoginForm from '@/components/LoginForm';
import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-8">
            Sistema de Gerenciamento de Usuários
          </h1>
          <div className="space-x-4">
            <Link
              href="/login"
              className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              Login
            </Link>
            <Link
              href="/"
              className="inline-block px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              Registrar
            </Link>
          </div>
        </div>
        <LoginForm />
      </div>
    </main>
  );
}