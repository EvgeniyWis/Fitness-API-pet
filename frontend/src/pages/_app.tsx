import type { AppProps } from "next/app";
import Head from "next/head";
import { Provider } from "react-redux";
import "@/shared/globals.css";
import { store } from "@/app/store";
import { MainLayout } from "@/widgets/layout/main-layout/ui";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <Provider store={store}>
      <Head>
        <title>Fitness App</title>
        <meta name="description" content="Fitness app frontend" />
      </Head>
      <MainLayout>
        <Component {...pageProps} />
      </MainLayout>
    </Provider>
  );
}
