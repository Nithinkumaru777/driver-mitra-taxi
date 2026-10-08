// Enquiry form logic, kept free of DOM so it runs in Node tests (scripts/enquiry.test.ts).
// To plug in a real backend or email service later, change submitEnquiry() only.
import { whatsappHref, type Copy } from '../content/site.ts';

export type Enquiry = { name: string; mobile: string; city: string; plan: string; licence: string; referral: string; message: string };
export type EnquiryErrors = Partial<Record<keyof Copy['form']['errors'], string>>;

/**
 * Indian mobile → 10 digits, or null if invalid. Accepts what drivers paste or type:
 * spaces/dashes, a +91 / 91 / 0 prefix. Must start with 6–9; rejects one digit repeated (9999999999).
 */
export function parseMobile(input: string): string | null {
  const digits = input.replace(/\D/g, '').replace(/^(91(?=\d{10}$)|0(?=\d{10}$))/, '');
  return /^[6-9]\d{9}$/.test(digits) && !/^(\d)\1{9}$/.test(digits) ? digits : null;
}

export function validateEnquiry(e: Enquiry, t: Copy): EnquiryErrors {
  const errors: EnquiryErrors = {};
  if (!e.name.trim()) errors.name = t.form.errors.name;
  if (!parseMobile(e.mobile)) errors.mobile = t.form.errors.mobile;
  if (!e.city.trim()) errors.city = t.form.errors.city;
  if (!e.plan) errors.plan = t.form.errors.plan;
  if (!e.licence) errors.licence = t.form.errors.licence;
  return errors;
}

/** The WhatsApp message: one "Label: value" line per field, labels from the copy file. Call only after validation passes. */
export function enquiryMessage(e: Enquiry, t: Copy): string {
  const f = t.form;
  const mobile = parseMobile(e.mobile)!;
  return [
    f.whatsappIntro,
    '',
    `${f.name}: ${e.name.trim()}`,
    `${f.mobile}: +91 ${mobile.slice(0, 5)} ${mobile.slice(5)}`,
    `${f.city}: ${e.city.trim()}`,
    `${f.plan}: ${t.plans.planTitle(Number(e.plan))}`,
    `${f.licence} ${e.licence}`,
    ...(e.referral.trim() ? [`${f.referralCode}: ${e.referral.trim()}`] : []),
    ...(e.message.trim() ? [`${f.message}: ${e.message.trim()}`] : []),
  ].join('\n');
}

/** Hands the enquiry off. Today: a wa.me link with the details pre-filled. Returns the link so the UI can offer it again. */
export function submitEnquiry(e: Enquiry, t: Copy): string {
  return whatsappHref(enquiryMessage(e, t));
}
