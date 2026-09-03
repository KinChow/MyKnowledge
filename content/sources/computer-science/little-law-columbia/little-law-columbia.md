---
archive_policy: text-only
attachments:
- filename: little-law-columbia.pdf
  kind: document
  media_type: application/pdf
  role: original
  sha256: sha256:bbc88a996da9ffaad473b073d46dafab1e54ace4f3e173b3a83cf34c9d6f734c
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-47e5f178256f
  position:
    end: 357
    start: 73
    type: TextPositionSelector
  quote_sha256: sha256:46e6c2bef8ab895f4e8e9073506335c8356776867a1abfe0688ab4bfb1c19646
  selector:
    exact: We consider here a famous and very useful law in queueing theory called
      Little's Law, also known as l = λw, which asserts that the time average number
      of customers in a queueing system, l, is equal to the rate at which customers
      arrive, λ, × the average sojourn time of a customer, w.
    prefix: 'Notes on Little''s Law (l = λw)


      '
    suffix: ' For example, in a four-year col'
    type: TextQuoteSelector
  selector_sha256: sha256:161219d8b2fcf0b28e3de09c8edfd23160a755ae6a014172d0b6a7248e3c220c
  snapshot_sha256: sha256:408794bd88c35946641905060169edf0e5172666a9e9857fe60c520676ff9159
extractor: marker/2.0.0
id: little-law-columbia
media_type: application/pdf
origin: external
raw_ref:
  path: archive/raw/bbc88a996da9ffaad473b073d46dafab1e54ace4f3e173b3a83cf34c9d6f734c.pdf
  sha256: sha256:bbc88a996da9ffaad473b073d46dafab1e54ace4f3e173b3a83cf34c9d6f734c
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: http://www.columbia.edu/~ks20/4106-18-Fall/Notes-LL.pdf
  url: http://www.columbia.edu/~ks20/4106-18-Fall/Notes-LL.pdf
schema_version: source/v1
snapshot_sha256: sha256:408794bd88c35946641905060169edf0e5172666a9e9857fe60c520676ff9159
source_type: doc
vault_id: public
---
## Copyright c 2017 by Karl Sigman

## 1 Notes on Little's Law (l = λw)

We consider here a famous and very useful law in queueing theory called Little's Law, also known as l = λw, which asserts that the time average number of customers in a queueing system, l, is equal to the rate at which customers arrive, λ, × the average sojourn time of a customer, w. For example, in a four-year college, in which (on average) 5000 first-year students enter per year, the average number of students present at this college is given by 5000 ×4 = 20, 000.<sup>1</sup> After presenting l = λw, we offer, in the same spirit, a more general law known as H = λG that allows one to analyze different queueing quantities of interest besides number in system, but is based on the same elementary principles and methods. Our presentation is based on a sample-path analysis and the reader should not assume apriori that any specific stochastic assumptions are in force. Imagine instead that a sample path is being studied of some stochastic queueing process.

## 1.1 Little's Law

We consider a queueing "system" in which customers arrive from the outside, spend some time in the system and then depart. C<sup>n</sup> denotes the n th customer, and this customer arrives and enters the system at time tn. The point process {t<sup>n</sup> : n ≥ 1} is assumed an increasing (to ∞) sequence of non-negative numbers with counting process {N(t) : t ≥ 0}; N(t) = max{n : t<sup>n</sup> ≤ t} (= 0 if there are no arrivals by time t), the number of arrivals during (0, t]. Upon entering the system, C<sup>n</sup> spends W<sup>n</sup> ≥ 0 units of time inside the system (Cn's sojourn time) and then departs the system at time t d <sup>n</sup> = t<sup>n</sup> + Wn. Note that the departure times are not necessarily ordered, which means that we do not require that customers depart in the same order that they arrived (think of a supermarket). {N<sup>d</sup> (t) : t ≥ 0} denotes the counting process for the departure times {t d <sup>n</sup>}; N<sup>d</sup> (t) = the number of customers who have departed by time t; note that N<sup>d</sup> (t) ≤ N(t), t ≥ 0.

A customer C<sup>n</sup> is in the system at time t if and only if t<sup>n</sup> ≤ t < t<sup>d</sup> <sup>n</sup> = t<sup>n</sup> +Wn, and we define L(t), the total number of customers in the system at time t, by

<sup>L</sup>(t) = <sup>X</sup><sup>∞</sup> n=1 I{t<sup>n</sup> ≤ t < t<sup>d</sup> (1) <sup>n</sup>}

= X {n:tn≤t} (2) I{W<sup>n</sup> > t − tn}

= N X (t) n=1 (3) I{W<sup>n</sup> > t − tn},

where I{A} denotes the indicator function for the event A: I{A} = 1 if A occurs; 0 otherwise. Define (when the limits exist)

λ def = lim t→∞ N(t) t (4) , the arrival rate into the system,

<sup>1</sup>Little's Law is named after John D.C. Little, who was the first to prove a version of it, in 1961. Little's original framework was stochastic however. In 1974 S. Stidham proved a sample-path version which is what we present here.

w def = limn→∞ 1 n Xn j=1 (5) W<sup>j</sup> , average sojourn time,

l def = lim t→∞ 1 t Z t 0 (6) L(s)ds, time average number in system.

Theorem 1.1 ( l = λw) If both λ and w exist and are finite, then l exists and l = λw.

l = λw is one of the most general and versatile laws in queueing theory, and, if used in clever ways, can lead to remarkably simple derivations. The trick is to choose what the "system" is, and what the arrivals to this system are. For example, given a complicated network of queues, the "system" can be the waiting area of an isolated node of interest, or it can be one (or all together) of the service areas, etc.

The area under the path of L(s) from 0 to t, R t <sup>0</sup> L(s)ds, is simply the sum of whole and partial sojourn times (e.g., rectangles of height 1 and lengths W<sup>j</sup> ). This is because: A customer C<sup>j</sup> is in the system at time t if and only if t<sup>j</sup> ≤ t < t<sup>d</sup> <sup>j</sup> = tj+W<sup>j</sup> , so they contribute height 1 to the path of {L(s)} all throughout their sojourn time W<sup>j</sup> yielding an area under {L(s)} of size W<sup>j</sup> ×1 = W<sup>j</sup> . If the system is empty at time t, then the area is exactly R <sup>t</sup> <sup>0</sup> L(s)ds = W1+· · ·+WN(t) ; otherwise some partial pieces must be considered. The following inequality is easily derived:

X {j:t d <sup>j</sup> ≤t} W<sup>j</sup> ≤ Z t 0 L(s)ds ≤ X {j:tj≤t} W<sup>j</sup> = N X (t) j=1 (7) W<sup>j</sup> .

To see this:

Z t 0 L(s)ds = Z t 0 { X {j:tj≤s≤t} (8) I{W<sup>j</sup> > s − tj}}ds

= X Z t tj (9) I{W<sup>j</sup> > s − tj}ds

{j:tj≤t} = X {j:tj≤t} (10) min{W<sup>j</sup> , t − tj}.

Since min{W<sup>j</sup> , t − tj} ≤ W<sup>j</sup> , the upper bound in (7) is immediate. For the lower bound

X {j:tj≤t} min{W<sup>j</sup> , t − tj} = X {j:tj+Wj≤t} W<sup>j</sup> + X {j:tj≤t, tj+Wj>t} (11) t − t<sup>j</sup>

≥ X {j:tj+Wj≤t} W<sup>j</sup> = X {j:t d <sup>j</sup> ≤t} (12) W<sup>j</sup> .

Dividing the upper bound by t, and re-writing 1/t = (N(t)/t)(1/N(t)), we obtain

( N(t) t ) 1 N(t) N X (t) j=1 W<sup>j</sup> .

Taking the limit as t−→∞ yields λw, due to the assumed existence of the two limts in (4) and (5) for λ and w (and their assumed finiteness). Thus the proof of l = λw can be completed by showing that the lower bound in (7) when divided by t converges to λw as well, that is, we must show that

lim t→∞ 1 t X {j:t d <sup>j</sup> ≤t} (13) W<sup>j</sup> = λw.

Lemma 1.1 If λ and w exists and are finite, then

limn→∞ W<sup>n</sup> n (14) = 0,

limn→∞ W<sup>n</sup> tn (15) = 0.

Proof :

W<sup>n</sup> n = 1 n Xn j=1 W<sup>j</sup> − 1 n nX−1 j=1 (16) W<sup>j</sup>

= 1 n Xn j=1 W<sup>j</sup> − ( n − 1 n )( <sup>1</sup> n − 1 ) nX−1 j=1 (17) W<sup>j</sup>

(18) → w − w = 0,

by (5) and finiteness of w. (14) is thus proved.

From (4) it follows that N(tn)/t<sup>n</sup> → λ because it is assumed that t<sup>n</sup> → ∞. Assuming that the arrival times are strictly increasing yields N(tn) = n and thus that

n tn = N(tn) tn → λ.

If the arrival times are not strictly increasing (so-called batch arrivals), then

n tn ≤ N(tn) tn → λ.

Thus in either case, from (14)

W<sup>n</sup> tn = W<sup>n</sup> n n tn ≤ W<sup>n</sup> n N(tn) tn → 0 λ = 0,

because λ is assumed finite. (15) is thus proved.

We are now prepared to finish the proof of l = λw: Proof :[l = λw] To prove (13) it suffices to prove

lim t→∞ 1 t X {j:t d <sup>j</sup> ≤t} (19) W<sup>j</sup> ≥ λw,

because we already established λw as an upper bound.

To this end, choose any > 0 no matter how small. From Lemma 1.1 there exists an integer m such that W<sup>j</sup> ≤ t<sup>j</sup> , j ≥ m, and thus that t d <sup>j</sup> = t<sup>j</sup> + W<sup>j</sup> ≤ (1 + )t<sup>j</sup> , j ≥ m.

Thus

{j : t d <sup>j</sup> ≤ t} ⊃ {j : j ≥ m, (1 + )t<sup>j</sup> ≤ t} = {j : j ≥ m, t<sup>j</sup> ≤ t 1 + },

from which it follows that

X {j:t d <sup>j</sup> ≤t} W<sup>j</sup> ≥ N( t 1+ X ) j=m W<sup>j</sup> .

The rhs of the above can be re-written as

N( 1+ X ) j=1 W<sup>j</sup> − mX−1 j=1 W<sup>j</sup> .

Dividing the first piece by t and letting t → ∞ yields λw/(1 + ) by the same argument used on the upper bound in (7). The second piece is a constant hence when divided by t, tends to 0. Thus we conclude that for any > 0,

lim t→∞ 1 t X {j:t d <sup>j</sup> ≤t} W<sup>j</sup> ≥ λw/(1 + ).

Since > 0 was chosen arbitrary, we conclude that (19) holds.

A consequence of the proof of Theorem 1.1 (l = λw) is

Proposition 1.1 If λ exists and is finite, and if Wn/n → 0, then

lim t→∞ N<sup>d</sup> (t) t = λ,

the departure rate exists and equals the arrival rate λ: Departure rate = arrival rate.

Proof : (15) followed from (14) only (a condition that is weaker than assuming w exists and is finite); hence as in the proof of l = λw, for every > 0 there exists an integer m such that N<sup>d</sup> (t) ≥ N(t/(1 + )) − m, yielding

lim t→∞ N<sup>d</sup> (t) t ≥ λ.

Since N<sup>d</sup> (t) ≤ N(t), limt→∞ N<sup>d</sup>(t) <sup>t</sup> ≤ limt→∞ N(t) <sup>t</sup> = λ; the upper bound holds as well yielding the result.

## 1.2 Applications of l = λw

- 1. Q = λd: If we let the "system" be the queue area (where customers wait before entering service), then average sojourn time is average delay in queue, d, l becomes average number waiting in queue, Q, and l = λw takes on the form Q = λd.

- 2. Infinite server queue: For any infinite server queue with arrival rate λ < ∞ and average service time 1/µ < ∞, l exists and l = ρ = λ/µ, because w = 1/µ here: W<sup>n</sup> = Sn.
- 3. Proportion of time the server is busy in a single-server queue: Customers arrive to the queue at rate λ < ∞ and have average service time 1/µ < ∞. Let λ<sup>s</sup> denote the rate at which customers enter service. Letting the "system" be the server, and letting Ls(t) denote the number of customers in service at time t, with time-average ls, we conclude that l<sup>s</sup> = λs(1/µ), because W<sup>n</sup> = S<sup>n</sup> here. It can be proved that λ<sup>s</sup> = λ when ρ < 1 and λ<sup>s</sup> = µ when ρ ≥ 1. Thus l<sup>s</sup> = ρ if ρ < 1; l<sup>s</sup> = 1 if ρ ≥ 1. But since Ls(t) = 1 if the server is busy at time t, and Ls(t) = 0 if the server is idle at time t, we conclude (from the fact that l<sup>s</sup> is a time average) that l<sup>s</sup> is in fact the long run proportion of time the server is busy:

The long-run proportion of time the server is busy in a single-server queue = min{1, ρ}.