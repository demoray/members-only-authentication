# SCA Member Portal Authentication

At the request of the Society Marshal, the head of all marshal activities within
the SCA, with the acknowledgement and support of the Society Vice President of
IT, I began work to expand support for an web application I had developed for
the Kingdom of Atlantia.  The application is used by Atlantia to manage warrant
rosters, authorization information, and to track incident reports.

Working through multiple challenges, including resource allocation, software
licensing, risk assessments, etc; I deployed a live "demo" in late 2019 on an
SCA-IT provided web server. 

While I had previously interacted with Atlantia's webminister about providing an
[OAuth](https://en.wikipedia.org/wiki/OAuth) endpoint for centralized
authentication, no such Single Signon solution was available for the SCA as a
whole.

On the weekend of January 11th 2020, I investigated if a "Single Sign-On"
implementation using the SCA's Members Portal as an authoritative central portal
of identity was possible.  While I was able to successfully implement a proof of
concept, which will be detailed below, the performance requirements for the
implementation ultimately untenable.

From here, we will discuss the a brief background on "Single Sign-On", examples
used in the public space, the technical details of the implementation, and a
brief discussion on risks, and an evaluation if this is a vulnerability.

## Background on Single-Sign-On
Currently, each kingdom, and often every application used by each kingdom, must
provide their own mechanism for authenticating users to their resources. As I
was developing and deploying an application for use for all SCA members on the
behalf of the VP of IT for the SCA, I thought it prudent to investigate if the
SCA's member portal could be used as an external source for authentication.

Wikipedia describes the [benefits of single sign-on](https://en.wikipedia.org/wiki/Single_sign-on) thusly:
* Mitigate risk for access to 3rd-party sites (user passwords not stored or managed externally)
* Reduce password fatigue from different username and password combinations
* Reduce time spent re-entering passwords for the same identity
* Reduce IT costs due to lower number of IT help desk calls about passwords

## Current examples uses in the public space
There are multiple instances of using an external source for identity management as a feature.  This idea is used throughout the internet for positive benefits for decades commercially and in the open source software world.

1. [Owncloud](https://github.com/owncloud/user_external), a Dropbox-like software project used by hundreds of thousands of businesses and the Department of Defense, provides calls this functionality "External User Authentication". This functionality has been in active use as part of Owncloud since 2012.
2. [PHP-IMAP-AUTH](https://github.com/rmader/php-imap-auth) is an open source plugin to Nginx, an extremely popular web server software, provides this functionality as a mechanism to authenticate access to websites.  This functionality was initially published in 2017.
3. [Django-telegram-login](https://github.com/dmytrostriletskyi/django-telegram-login) is an open-source application that demonstrates this functionality using Telegram's login capabilities published in 2018. 
4. Dokuwiki, a popular Wiki platform, had a [user-contributed module](https://gist.github.com/vjt/804858) that demonstrates this functionality in 2012 and [recreated in 2017](https://github.com/marcofenoglio/dokuwiki-plugin-authimap2).
5. phpIPAM, an IP address management application used by multiple ISPs, had a [plugin to provide this functionality](https://github.com/phpipam/phpipam/pull/938) contributed by one of phpIPAM’s users in 2017.
6. [MultiLogin](https://multilogin.com/) is a large commercial company that allows MultiLogin customers to use this functionality to share sessions to third-party resources, such as allowing everyone in a company's marketing department access to the company's twitter account.

## Development Background
During my development, I identified that the Member Portal used [GWT-RPC](https://en.wikipedia.org/wiki/Google_Web_Toolkit), a publicly documented plain text communications protocol, to perform the authentication.  GWT-RPC refers to “Google Web Toolkit, Remote Procedure Call”. This was a commonly used software package built by Google to allow web browsers to communicate with web servers.  Early versions of Gmail used GWT-RPC as a communications protocol, with multiple independently developed third-party capabilities built on top of Google’s use of GWT-RPC to extend Gmail.

My initial attempt to implement Single Sign-On was done in [Selenium](https://selenium.dev/), a popular browser automation toolkit used for automatically interacting with web applications . With Selenium, a developer can write software that interacts with a website like a user. Selenium is directly supported by Google, Facebook, and Mozilla to automatically interact with their websites.  

While GWT-RPC is a publicly documented protocol, it is built on extensive use of Javascript.  Replacing the Selenium implementation with a reimplementation of the Javascript APIs was possible, it would have required a significant amount of work, and would have been difficult to maintain.  Additionally, the Selenium implementation would have required a significant amount of resources to run, as each user would have required a new instance of Chrome to be launched.

As such, this approach was abandoned.

## Discussion on Exposure & Risk
Let's talk about the exposures and risks of this capability, if deployed compared to creating an application specific authentication system:

1. The software was to run on [https://\[REDACTED\].sca.org/]() an official Society owned web server, with credentials passed to [https://\[REDACTED\].sca.org/](). All credentials would only pass through Society managed resources using Society managed HTTPS encryption.  This exposes no substantive additional risk to users.
2. Membership data would be retrieved during the user's authentication process. Without this, the membership information would be provided to the system regardless, but with measurable burden to each kingdom. This exposes no substantive additional risk to users.
3. Users would be required to manage fewer passwords. This is a measurable reduction in risk to users.
4. User credentials would be stored in one fewer server. This is a measurable reduction in risk to users.
5. Admins of the members portal could control logins to an additional SCA official resource, with sensitive information such as PII and incident reports. An example immediate benefit would be providing the SCA Corporate office the ability to trivially prevent logins to persons banned from the society. Without this capability, a banned member would be able to leverage the system until each kingdom's proceeding monthly data process completes. This is a measurable reduction of exposure to liability to the SCA.

As there was no additional exposure or risk, with no public information used or disclosed, the society only stood to benefit from building this capability.

## Discussions on what makes up a Vulnerability

The [CIA Triad model](https://www.techrepublic.com/blog/it-security/the-cia-triad/) is a commonly used method to describe what makes up a vulnerability using the areas of “confidentiality, integrity, and availability”.  Let’s discuss each of these areas as it relates to a single sign-on capability for use within an SCA application.

### Confidentiality
The key importance is protecting sensitive information from unauthorized access.
In this case, the sensitive data at question is a user's membership information.
As this capability was developed as part of a system that already includes the
user’s membership information, confidentiality is not compromised.

### Integrity
The system could be used to alter one instance of a member’s personal records
(such as their address) after a user has provided their credentials. However,
the warrant system already maintains a copy of the member’s personal records for
use in verifying warrants. Given the intent of the warrant system is to act as a
first class source of truth for verifying membership with respect to warrants
and authorizations, with the information already provided by the SCA membership
office, this provides no meaningful additional risk.

### Availability
At no point has any availability of the members portal been impacted for this
issue.  Under these areas, attempting to build a Single Sign-On solution for use
in SCA resources on SCA-Corporate computers is not a vulnerability.