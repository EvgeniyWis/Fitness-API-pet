import React from "react";
import Link from "next/link";

interface AuthFormContainerProps {
  title: string;
  children: React.ReactNode;
  footerText: string;
  footerLinkText: string;
  footerLinkHref: string;
}

export const AuthFormContainer: React.FC<AuthFormContainerProps> = ({
  title,
  children,
  footerText,
  footerLinkText,
  footerLinkHref,
}) => {
  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          {title}
        </h1>

        {children}

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            {footerText}{" "}
            <Link
              href={footerLinkHref}
              className="font-medium text-blue-600 hover:text-blue-700"
            >
              {footerLinkText}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
