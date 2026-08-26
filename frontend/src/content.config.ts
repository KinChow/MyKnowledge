import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

// Starlight owns Markdown parsing and static route generation. The release
// preparation step is the only writer of this collection and only copies
// allowlisted public-projection items into it.
export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema(),
  }),
};
