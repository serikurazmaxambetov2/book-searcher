import { Injectable } from '@nestjs/common';
import { ElasticsearchService } from '@nestjs/elasticsearch';
import { BookCreateDto } from 'src/book/dto/book-create.dto';

@Injectable()
export class SearchService {
  constructor(private elasticsearchService: ElasticsearchService) {}

  async createIndex() {
    return await this.elasticsearchService.indices.create({
      index: 'book',
      mappings: {
        properties: {
          title: {
            type: 'text',
          },
          description: {
            type: 'text',
          },
          id: {
            type: 'long',
          },
        },
      },
    });
  }

  async getIndex() {
    return await this.elasticsearchService.indices.get({
      index: 'book',
      ignore_unavailable: true,
    });
  }

  async deleteIndex() {
    return await this.elasticsearchService.indices.delete({ index: 'book' });
  }

  async search(text: string) {
    return await this.elasticsearchService.search({
      index: 'book',
      query: {
        bool: {
          should: [
            {
              match: {
                title: {
                  query: text,
                  fuzziness: 'AUTO',
                  boost: 2.0,
                },
              },
            },
            {
              match: {
                description: {
                  query: text,
                  fuzziness: 'AUTO',
                },
              },
            },
          ],
        },
      },
    });
  }

  async addDocument(document: BookCreateDto) {
    return await this.elasticsearchService.index({
      index: 'book',
      document,
    });
  }
}
