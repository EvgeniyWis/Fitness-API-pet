import type { AppProps } from "next/app";
import Head from "next/head";
import "@/shared/globals.css";
import { MainLayout } from "@/widgets/layout/main-layout/ui";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Fitness App</title>
        <meta name="description" content="Fitness app frontend" />
      </Head>
      <MainLayout>
        <Component {...pageProps} />
      </MainLayout>
    </>
  );
}
