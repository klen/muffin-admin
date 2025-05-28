import { defaultDarkTheme, defaultLightTheme } from "react-admin"

export const muffinLightTheme: typeof defaultLightTheme = {
  ...defaultLightTheme,
  components: {
    ...defaultLightTheme.components,
    RaMenuItemLink: {
      styleOverrides: {
        root: {
          "&.RaMenuItemLink-active": {
            borderRadius: "4px",
            backgroundColor: "#f0f0f0",
          },
        },
      },
    },
  },
}

export const muffinDarkTheme: typeof defaultDarkTheme = {
  ...defaultDarkTheme,
  components: {
    ...defaultDarkTheme.components,
    RaMenuItemLink: {
      styleOverrides: {
        root: {
          "&.RaMenuItemLink-active": {
            borderRadius: "4px",
            backgroundColor: "#424242",
          },
        },
      },
    },
  },
}
