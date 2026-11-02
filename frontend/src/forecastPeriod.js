function getJapanTodayISO(now = new Date()) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Tokyo",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const part = (type) => parts.find((item) => item.type === type)?.value || "";
  return `${part("year")}-${part("month")}-${part("day")}`;
}

export function getTomorrowISODate(now = new Date()) {
  const tomorrow = new Date(`${getJapanTodayISO(now)}T00:00:00Z`);
  tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
  return tomorrow.toISOString().slice(0, 10);
}

export function resolveForecastPeriod(appliedPeriod, tomorrow) {
  if (
    appliedPeriod &&
    typeof appliedPeriod.from === "string" &&
    typeof appliedPeriod.to === "string" &&
    appliedPeriod.from <= appliedPeriod.to
  ) {
    return { startDate: appliedPeriod.from, endDate: appliedPeriod.to };
  }
  return { startDate: tomorrow, endDate: tomorrow };
}
