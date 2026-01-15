"use client";

import Link from "next/link";
import { Button } from "@/shared/ui";

export const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-gray-900">
              Fitness App
            </Link>
          </div>

          <nav className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="outline" size="md">
                Войти
              </Button>
            </Link>
            <Link href="/register">
              <Button variant="primary" size="md">
                Регистрация
              </Button>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};
