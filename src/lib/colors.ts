import type { ColorMode } from "../components/ui/color-mode";
import type { Activity } from "./activity";

/** The type of color schemes. */
export interface ColorScheme {
  name: string;
  colorMode: ColorMode;
  backgroundColors: string[];
}

const classic: ColorScheme = {
  name: "Classic",
  colorMode: "light",
  backgroundColors: [
    "#23AF83",
    "#3E9ED1",
    "#AE7CB4",
    "#DE676F",
    "#E4793C",
    "#D7AD00",
    "#33AE60",
    "#F08E94",
    "#8FBDD9",
    "#A2ACB0",
  ],
};

const classicDark: ColorScheme = {
  name: "Classic (Dark)",
  colorMode: "dark",
  backgroundColors: [
    "#36C0A5",
    "#5EBEF1",
    "#CE9CD4",
    "#EA636B",
    "#FF995C",
    "#F7CD20",
    "#47CE80",
    "#FFAEB4",
    "#AFDDF9",
    "#C2CCD0",
  ],
};

const highContrast: ColorScheme = {
  name: "High Contrast",
  colorMode: "light",
  backgroundColors: [
    "#FF6B6B",
    "#FFD93D",
    "#4FC3F7",
    "#81C784",
    "#C580D1",
    "#FFADC5",
    "#309BF3",
    "#FF8A65",
  ],
};

const highContrastDark: ColorScheme = {
  name: "High Contrast (Dark)",
  colorMode: "dark",
  backgroundColors: [
    "#EB7070",
    "#FFE066",
    "#67D5E3",
    "#7BE27B",
    "#B584E6",
    "#FF85C0",
    "#66B2FF",
    "#FFA570",
  ],
};

/** The default color schemes. */
export const COLOR_SCHEME_PRESETS: ColorScheme[] = [
  classic,
  classicDark,
  highContrast,
  highContrastDark,
];

export const COLOR_SCHEME_DARK = classicDark;
export const COLOR_SCHEME_LIGHT = classic;
export const COLOR_SCHEME_DARK_CONTRAST = highContrastDark;
export const COLOR_SCHEME_LIGHT_CONTRAST = highContrast;

/** The default background color for a color scheme. */
export function fallbackColor(colorScheme: ColorScheme): string {
  return colorScheme.colorMode === "light" ? "#4A5568" : "#CBD5E0";
}

/** MurmurHash3, seeded with a string. */
function murmur3(str: string): () => number {
  let hash = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    hash = Math.imul(hash ^ str.charCodeAt(i), 3432918353);
    hash = (hash << 13) | (hash >>> 19);
  }
  return () => {
    hash = Math.imul(hash ^ (hash >>> 16), 2246822507);
    hash = Math.imul(hash ^ (hash >>> 13), 3266489909);
    return (hash ^= hash >>> 16) >>> 0;
  };
}

export const getDefaultColorScheme = (): ColorScheme => {
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const prefersConstrast = window.matchMedia(
    "(prefers-constrast: more)",
  ).matches;

  if (prefersConstrast) {
    if (prefersDark) {
      return COLOR_SCHEME_DARK_CONTRAST;
    } else {
      return COLOR_SCHEME_LIGHT_CONTRAST;
    }
  } else {
    if (prefersDark) {
      return COLOR_SCHEME_DARK;
    } else {
      return COLOR_SCHEME_LIGHT;
    }
  }
};

/**
 * Assign background colors to a list of activities. Mutates each activity
 * in the list.
 */
export function chooseColors(
  activities: Activity[],
  colorScheme: ColorScheme,
): void {
  // above this length, we give up trying to be nice:
  const colorLen = colorScheme.backgroundColors.length;
  const indices: number[] = [];
  for (const activity of activities) {
    if (activity.manualColor) continue;
    const hash = murmur3(activity.id);
    let index = hash() % colorLen;
    // try to pick distinct colors if possible; hash to try to make each
    // activity have a consistent color.
    while (indices.length < colorLen && indices.includes(index)) {
      index = hash() % colorLen;
    }
    indices.push(index);
    activity.backgroundColor = colorScheme.backgroundColors[index];
  }
}

/** Choose a text color for a background given by hex code color. */
export function textColor(color: string): string {
  const r = parseInt(color.substring(1, 3), 16);
  const g = parseInt(color.substring(3, 5), 16);
  const b = parseInt(color.substring(5, 7), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 128 ? "#000000" : "#ffffff";
}

/** Return a standard #AABBCC representation from an input color */
export function canonicalizeColor(code: string): string | undefined {
  code = code.trim();
  const fiveSix = code.match(/^#?[0-9a-f]{5,6}$/gi);
  if (fiveSix) {
    return code.startsWith("#") ? code : `#${code}`;
  }
  const triplet = code.match(/^#?[0-9a-f]{3}$/gi);
  if (triplet) {
    const expanded =
      code.slice(-3, -2) +
      code.slice(-3, -2) +
      code.slice(-2, -1) +
      code.slice(-2, -1) +
      code.slice(-1) +
      code.slice(-1);
    return code.startsWith("#") ? expanded : `#${expanded}`;
  }
  return undefined;
}

/** The Google calendar background color. */
// export const CALENDAR_COLOR = "#DB5E45";
