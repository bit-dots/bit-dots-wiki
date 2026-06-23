import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const wiki = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/wiki" }),
  schema: z.object({
    title: z.string().optional(),
    description: z.string().optional(),
    category: z.enum(['tech', 'finance', 'life', 'project']).optional(),
    tags: z.array(z.string()).optional(),
    author: z.string().optional(),
    pubDate: z.date().optional(),
    updatedDate: z.date().optional(),
    image: z.string().optional(),
    draft: z.boolean().optional().default(false),
  }),
});

export const collections = {
  wiki,
};
