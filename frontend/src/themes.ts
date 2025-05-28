import { defaultDarkTheme, defaultLightTheme } from "react-admin"

export const muffinLightTheme: typeof defaultLightTheme = {
  ...defaultLightTheme,
  components: {
    ...defaultLightTheme.components,
    RaMenuItemLink: {
      styleOverrides: {
        root: {
          "&.RaMenuItemLink-active": {
            backgroundColor: "#f0f0f0",
            borderRadius: "4px",
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
            backgroundColor: "#424242",
            borderRadius: "4px",
          },
        },
      },
    },
  },
}
