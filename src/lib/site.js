import business from '$lib/data/business.json';

export const SITE_URL = 'https://resolve.works';

/** Build a mailto: href with proper percent-encoding. */
export function mailtoHref(subject, body) {
  const { email } = business;
  return `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}

const MONTHS = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

/** Format an ISO date string as "Month D, YYYY" (locale-independent). */
export function formatDate(iso) {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso);
  const [, year, month, day] = match;
  return `${MONTHS[Number(month) - 1]} ${Number(day)}, ${year}`;
}
