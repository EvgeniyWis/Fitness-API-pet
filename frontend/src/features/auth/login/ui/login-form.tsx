"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { Button, Input, AuthFormContainer } from "@/shared/ui";
import { useLoginMutation } from "@/shared/api";
import { validateEmail, validatePassword } from "@/shared/lib";

export const LoginForm = () => {
  const router = useRouter();
  const [login, { isLoading }] = useLoginMutation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>(
    {},
  );
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setSubmitError(null);
    setSuccessMessage(null);

    const newErrors: { email?: string; password?: string } = {};
    const emailError = validateEmail(email);
    const passwordError = validatePassword(password, 1);

    if (emailError) newErrors.email = emailError;
    if (passwordError) newErrors.password = passwordError;

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const result = await login({
      username: email,
      password,
    }).unwrap();
    if (result.message) {
      if (rememberMe) {
        localStorage.setItem("rememberMe", "1");
      } else {
        localStorage.removeItem("rememberMe");
      }
      setSuccessMessage("Вход выполнен успешно. Перенаправление...");
      console.info("[Auth] Вход успешен:", email);
      setTimeout(() => router.push("/"), 1500);
    } else {
      setSubmitError(result.message ?? "Ошибка входа");
    }
  };

  return (
    <AuthFormContainer
      title="Вход"
      footerText="Нет аккаунта?"
      footerLinkText="Зарегистрироваться"
      footerLinkHref="/register"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="email"
          label="Email"
          placeholder="example@mail.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={errors.email}
          disabled={isLoading}
          autoComplete="email"
        />

        <Input
          type="password"
          label="Пароль"
          placeholder="Введите пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          error={errors.password}
          disabled={isLoading}
          autoComplete="current-password"
        />

        {successMessage && (
          <p className="text-sm text-green-600 font-medium" role="status">
            {successMessage}
          </p>
        )}
        {submitError && (
          <p className="text-sm text-red-600" role="alert">
            {submitError}
          </p>
        )}

        <div className="flex items-center justify-between">
          <label className="flex items-center">
            <input
              type="checkbox"
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            />
            <span className="ml-2 text-sm text-gray-600">Запомнить меня</span>
          </label>
          <Link
            href="/forgot-password"
            className="text-sm text-blue-600 hover:text-blue-700"
          >
            Забыли пароль?
          </Link>
        </div>

        <Button
          type="submit"
          variant="primary"
          size="lg"
          className="w-full"
          disabled={isLoading}
        >
          {isLoading ? "Вход..." : "Войти"}
        </Button>
      </form>
    </AuthFormContainer>
  );
};
