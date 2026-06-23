/**
 * Remark plugin: transforms VitePress <Badge> raw HTML into <span class="badge">.
 * Operates at the remark level because rehype-raw runs after user rehype plugins
 * in Astro's pipeline.
 */
import { visit } from 'unist-util-visit';

const VALID_TYPES = new Set(['tip', 'info', 'warning']);

export function rehypeBadges() {
  return (tree) => {
    visit(tree, 'html', (node, index, parent) => {
      if (!parent || index === undefined) return;

      const badgeRegex = /<Badge\s+type="(\w+)"\s+text="([^"]*)"\s*\/?>/g;
      let result = '';
      let lastIndex = 0;
      let replaced = false;

      let match;
      while ((match = badgeRegex.exec(node.value)) !== null) {
        const rawType = match[1];
        const text = match[2];
        const typeClass = VALID_TYPES.has(rawType) ? rawType : 'tip';

        result += node.value.slice(lastIndex, match.index);
        result += `<span class="badge ${typeClass}">${text}</span>`;
        lastIndex = match.index + match[0].length;
        replaced = true;
      }

      if (!replaced) return;

      result += node.value.slice(lastIndex);
      parent.children[index] = { type: 'html', value: result };
    });
  };
}
