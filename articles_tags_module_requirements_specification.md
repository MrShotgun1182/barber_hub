# Software Requirements Specification (SRS)
## Articles & Tags Module — Barber Hub

**Date:** October 13, 2026  
**Project:** Barber Hub Platform  
**Document Status:** Approved  

---

## 1. Executive Overview

The **Articles & Tags Module** introduces a full-featured blogging, news, and educational content engine to the Barber Hub platform. It allows barbers and salon managers to publish articles, grooming guides, and salon updates to improve search engine optimization (SEO), foster customer engagement, and showcase staff expertise.

The workflow enforces an editorial review process: content authored or edited by barbers enters a moderation pipeline managed exclusively by salon administrators before becoming publicly accessible.

---

## 2. Core Workflows & Operations

### 2.1. Tag Management Pipeline
* A standalone `tags` application handles categorization tags.
* Creation, editing, and deletion of tags are **restricted exclusively to Managers**.
* Barbers can assign existing tags to their articles but cannot create new tags.

### 2.2. Editorial & Publishing Lifecycle
1. **Creation/Edit by Barber:** A barber creates or edits an article. Upon saving, the article's status automatically transitions to `Pending`.
2. **Manager Moderation:** The manager reviews `Pending` articles and can perform one of the following actions:
   * **Approve/Publish (`Published`):** Makes the article visible on the public storefront.
   * **Reject (`Rejected`):** Rejects the article and optionally attaches feedback/reasons for the barber to correct.
   * **Archive (`Archived`):** Hides a previously published article from the public view without deleting it.
   * **Delete:** Permanently removes the article from the database.
3. **Direct Publication by Manager:** Articles created directly by managers bypass the moderation queue and can be published immediately.
4. **Featured Content Selection:** Managers can toggle the `Is Featured` flag on any article to highlight it prominently on the customer-facing blog page.

---

## 3. Detailed Data Models

### 3.1. Tag Entity (`tags` App)
| Field | Type | Rules / Constraints |
| --- | --- | --- |
| `id` | Identifier | Primary Key |
| `name` | String | Required, Unique, Max 50 chars |
| `slug` | String | Required, Unique, URL-friendly |

### 3.2. Article Entity (`articles` App)
| Field | Type | Rules / Constraints |
| --- | --- | --- |
| `id` | Identifier | Primary Key |
| `title` | String | Required, Max 255 chars |
| `slug` | String | Required, Unique, Auto-generated for SEO |
| `author` | Foreign Key | References `User` (Barber or Manager) |
| `cover_image` | Image Upload | **Required**, Main display image |
| `gallery` | One-to-Many / Image List | Optional, Collection of supplementary images |
| `content` | Rich Text / HTML | Required, Full article body |
| `tags` | Many-to-Many | References `Tag` entity |
| `is_featured` | Boolean | Default `False`. **Editable by Manager only** |
| `views_count` | Integer | Default `0`. Incremented on public page views |
| `status` | Enum | Options: `Draft`, `Pending`, `Published`, `Rejected`, `Archived` |
| `rejection_reason` | Text | Optional notes provided by Manager upon rejection |
| `created_at` | Timestamp | Auto-generated on creation |
| `updated_at` | Timestamp | Auto-updated on revision |
| `published_at` | Timestamp | Nullable, recorded upon first publication |

---

## 4. Role & Access Control Matrix

| Feature / Action | Customer / Public | Barber | Manager |
| --- | :---: | :---: | :---: |
| Browse Published & Featured Articles | ✅ | ✅ | ✅ |
| Search & Filter Articles | ✅ | ✅ | ✅ |
| Create / Edit / Delete Tags | ❌ | ❌ | ✅ |
| Create / Edit Own Articles | ❌ | ✅ | ✅ |
| Delete Own Articles | ❌ | ✅ | ✅ |
| View Own Article Analytics (Views) | ❌ | ✅ | ✅ |
| Moderate Articles (`Publish`, `Reject`, `Archive`) | ❌ | ❌ | ✅ |
| Provide Rejection Feedback | ❌ | ❌ | ✅ |
| Mark Article as Featured | ❌ | ❌ | ✅ |
| Manage / Delete Articles of Other Authors | ❌ | ❌ | ✅ |

---

## 5. UI/UX Functional Specifications

### 5.1. Customer Storefront (`/articles`)
* **Featured Section:** Highlights articles marked with `is_featured = True` in a banner or carousel at the top.
* **Article Grid:** Displays cards for `Published` articles containing the cover image, title, author name, publication date, tags, and view count.
* **Filtering & Search Toolbar:**
  * Keyword search (searches title and body text).
  * Filter by Tag.
  * Filter by Author (Barber/Manager).
  * Sort options: "Newest First", "Most Viewed".
* **Detail Page (`/articles/<slug>`):**
  * Displays full article content, cover image, image gallery slider, author bio, tags, and view count.
  * Automatically increments `views_count` upon page load.

### 5.2. Barber Panel (`/barber/articles`)
* **Article List View:** Displays a tabular list of articles authored by the logged-in barber.
  * Columns: Title, Status Badge, View Count, Created Date, Actions.
  * Displays rejection notes if status is `Rejected`.
* **Editor Interface:**
  * Form fields for Title, Cover Image upload, Gallery uploads, Tag selector, and Rich Text Editor for Content.
  * Saving any changes sets/resets the status to `Pending` for moderation.

### 5.3. Manager Panel (`/manager/articles` & `/manager/tags`)
* **Tag Management Section:** Interface to Add, Edit, or Delete tags.
* **Moderation Queue:**
  * Tabbed or filterable view for `Pending`, `Published`, `Rejected`, and `Archived` articles across all authors.
  * **Quick Actions:** Single-click approval (`Publish`), Rejection with modal input for feedback, Archiving, and Deletion.
  * Toggle button for setting/unsetting the `Featured` status.
* **Direct Article Publishing:** Allows managers to write and publish articles instantly without entering the pending queue.

---

## 6. Article Status Lifecycle Diagram

```
 [Barber Creates / Edits Article] ───>  Pending (In Review)  <─── [Barber Re-edits]
                                              │
                  ┌───────────────────────────┼───────────────────────────┐
                  ▼                           ▼                           ▼
             Published                    Rejected                    Archived
        (Visible to Public)       (Feedback sent to Barber)    (Hidden from Public)
                  │                           │                           │
                  └───────────────────────────┴───────────────────────────┘
                                              │
                                              ▼
                                   [Permanent Manager Delete]
```